from fastapi import APIRouter, Depends, HTTPException, Body, WebSocket, WebSocketDisconnect
from typing import Optional, List, Dict, Any
from uuid import uuid4
from datetime import datetime, timedelta
import random
import string
import logging
import json

from app.middleware.user import Middleware as UserMiddleware
from app.core.db import get_db
from app.utils.JWT import verify_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/contest", tags=["Contests"])
db = get_db()


# ─── WebSocket Connection Manager for Contests ─────────────────────────────────

class ContestWebSocketManager:
    def __init__(self):
        # room_code -> set of WebSockets
        self.connections: Dict[str, set[WebSocket]] = {}

    async def connect(self, room_code: str, websocket: WebSocket):
        await websocket.accept()
        if room_code not in self.connections:
            self.connections[room_code] = set()
        self.connections[room_code].add(websocket)
        logger.info(f"WS connected to contest room {room_code}. Count: {len(self.connections[room_code])}")

    async def disconnect(self, room_code: str, websocket: WebSocket):
        if room_code in self.connections:
            self.connections[room_code].discard(websocket)
            if not self.connections[room_code]:
                del self.connections[room_code]
        logger.info(f"WS disconnected from contest room {room_code}")

    async def broadcast(self, room_code: str, message: dict):
        if room_code in self.connections:
            dead = set()
            for ws in self.connections[room_code]:
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.add(ws)
            for ws in dead:
                self.connections[room_code].discard(ws)
            if room_code in self.connections and not self.connections[room_code]:
                del self.connections[room_code]

    async def broadcast_contest_update(self, room_code: str, message: dict):
        await self.broadcast(room_code, message)


contest_ws_manager = ContestWebSocketManager()


# ─── Helper function to update contest score ───────────────────────────────────

async def record_contest_submission(
    db,
    contest_id: str,
    user_id: str,
    problem_slug: str,
    verdict: str,
    score: float,
    passed: int,
    total: int,
    submission_id: str,
    runtime_ms: Optional[float] = None,
    memory_mb: Optional[float] = None
):
    contest = await db.contests.find_one({"contest_id": contest_id})
    if not contest:
        contest = await db.contests.find_one({"room_code": contest_id})

    if not contest:
        logger.warning(f"Contest {contest_id} not found for recording submission")
        return

    now = datetime.utcnow()
    start_time = contest.get("start_time")
    elapsed_seconds = 0
    if start_time:
        if isinstance(start_time, str):
            from dateutil.parser import parse
            start_time = parse(start_time)
        elapsed_seconds = int((now - start_time).total_seconds())

    participants = contest.get("participants", [])
    updated = False

    for p in participants:
        if str(p.get("user_id")) == str(user_id):
            scores = p.setdefault("scores", {})
            prob_score = scores.setdefault(problem_slug, {
                "solved": False,
                "solved_at": None,
                "attempts": 0,
                "score": 0.0,
                "submission_id": None
            })
            prob_score["attempts"] += 1
            if verdict == "accepted":
                prev_runtime = prob_score.get("runtime_ms")
                is_more_optimized = prev_runtime is None or (runtime_ms is not None and runtime_ms < prev_runtime)
                
                if not prob_score["solved"] or is_more_optimized:
                    prob_score["solved"] = True
                    prob_score["solved_at"] = now.isoformat()
                    # Award 100 points for solved, minus penalty for attempts
                    prob_score["score"] = max(50.0, 100.0 - (prob_score["attempts"] - 1) * 5.0)
                    prob_score["submission_id"] = submission_id
                    if runtime_ms is not None:
                        prob_score["runtime_ms"] = runtime_ms
                    if memory_mb is not None:
                        prob_score["memory_mb"] = memory_mb
            else:
                prob_score["submission_id"] = submission_id

            # Recalculate totals
            p["total_score"] = int(sum(s.get("score", 0.0) for s in scores.values()))
            solved_times = [s["solved_at"] for s in scores.values() if s.get("solved") and s.get("solved_at")]
            if solved_times:
                p["finish_time"] = max(solved_times)

            updated = True
            break

    if updated:
        await db.contests.update_one(
            {"_id": contest["_id"]},
            {"$set": {"participants": participants}}
        )

        # Broadcast the updated standings to all players in the contest room
        room_code = contest.get("room_code") or contest.get("contest_id")
        await contest_ws_manager.broadcast_contest_update(room_code, {
            "type": "leaderboard_update",
            "participants": [
                {
                    "user_id": p.get("user_id"),
                    "username": p.get("username"),
                    "total_score": p.get("total_score", 0),
                    "disqualified": p.get("disqualified", False),
                    "finish_time": p.get("finish_time"),
                    "warnings_count": len(p.get("warnings", []))
                } for p in participants
            ]
        })


# ─── HTTP Endpoints ────────────────────────────────────────────────────────────

@router.post("/create")
async def create_contest(
    payload: dict = Body(...),
    user_auth=Depends(UserMiddleware.me)
):
    user = user_auth["user"]
    title = payload.get("title", "Speed Coding Arena")
    description = payload.get("description", "Solve challenges as fast as possible without cheating.")
    challenges = payload.get("challenges", ["build-a-rate-limiter"])
    duration_minutes = int(payload.get("duration_minutes", 30))
    contest_type = payload.get("contest_type", "1v1")  # "1v1" | "open_world" | "official"

    # Generate 6-digit room code for rooms
    room_code = None
    if contest_type in ["1v1", "open_world"]:
        room_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    contest_id = str(uuid4())

    # Build initial participant list
    participants = [
        {
            "user_id": str(user["user_id"]),
            "username": user["username"],
            "full_name": user.get("full_name"),
            "joined_at": datetime.utcnow().isoformat(),
            "disqualified": False,
            "warnings": [],
            "scores": {},
            "total_score": 0,
            "finish_time": None
        }
    ]

    doc = {
        "contest_id": contest_id,
        "room_code": room_code,
        "title": title,
        "description": description,
        "challenges": challenges,
        "duration_minutes": duration_minutes,
        "contest_type": contest_type,
        "creator_id": str(user["user_id"]),
        "creator_username": user["username"],
        "status": "lobby" if contest_type != "official" else "active",
        "start_time": datetime.utcnow().isoformat() if contest_type == "official" else None,
        "end_time": (datetime.utcnow() + timedelta(minutes=duration_minutes)).isoformat() if contest_type == "official" else None,
        "participants": participants,
        "created_at": datetime.utcnow().isoformat()
    }

    await db.contests.insert_one(doc)
    doc.pop("_id", None)
    return {"success": True, "data": doc}


@router.get("/active")
async def get_active_contests(user_auth=Depends(UserMiddleware.me)):
    # Fetch official contests and open world lobbies
    cursor = db.contests.find({
        "status": {"$in": ["lobby", "active"]},
        "$or": [
            {"contest_type": "official"},
            {"contest_type": "open_world"}
        ]
    }).sort("created_at", -1)
    
    contests = []
    async for doc in cursor:
        doc.pop("_id", None)
        contests.append(doc)
    return {"success": True, "data": contests}


@router.get("/{code_or_id}")
async def get_contest_details(code_or_id: str, user_auth=Depends(UserMiddleware.me)):
    doc = await db.contests.find_one({
        "$or": [
            {"room_code": code_or_id.upper()},
            {"contest_id": code_or_id}
        ]
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Contest not found")
    
    doc.pop("_id", None)
    return {"success": True, "data": doc}


@router.post("/{code_or_id}/join")
async def join_contest(code_or_id: str, user_auth=Depends(UserMiddleware.me)):
    user = user_auth["user"]
    doc = await db.contests.find_one({
        "$or": [
            {"room_code": code_or_id.upper()},
            {"contest_id": code_or_id}
        ]
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Contest not found")

    if doc["status"] == "completed":
        raise HTTPException(status_code=400, detail="Contest already completed")

    # If it is 1v1, verify capacity
    if doc["contest_type"] == "1v1" and len(doc["participants"]) >= 2:
        # Check if already joined
        already_joined = any(str(p["user_id"]) == str(user["user_id"]) for p in doc["participants"])
        if not already_joined:
            raise HTTPException(status_code=400, detail="1v1 Room is full")

    # Add player if not already in participants
    user_id_str = str(user["user_id"])
    already_joined = any(str(p["user_id"]) == user_id_str for p in doc["participants"])

    if not already_joined:
        new_participant = {
            "user_id": user_id_str,
            "username": user["username"],
            "full_name": user.get("full_name"),
            "joined_at": datetime.utcnow().isoformat(),
            "disqualified": False,
            "warnings": [],
            "scores": {},
            "total_score": 0,
            "finish_time": None
        }
        await db.contests.update_one(
            {"_id": doc["_id"]},
            {"$push": {"participants": new_participant}}
        )
        # Fetch updated doc
        doc = await db.contests.find_one({"_id": doc["_id"]})

        # Broadcast user joined over WS
        room_key = doc.get("room_code") or doc.get("contest_id")
        await contest_ws_manager.broadcast(room_key, {
            "type": "user_joined",
            "username": user["username"],
            "participants": [
                {"user_id": p["user_id"], "username": p["username"]}
                for p in doc["participants"]
            ]
        })

    doc.pop("_id", None)
    return {"success": True, "data": doc}


@router.post("/{code_or_id}/start")
async def start_contest(code_or_id: str, user_auth=Depends(UserMiddleware.me)):
    user = user_auth["user"]
    doc = await db.contests.find_one({
        "$or": [
            {"room_code": code_or_id.upper()},
            {"contest_id": code_or_id}
        ]
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Contest not found")

    if str(doc["creator_id"]) != str(user["user_id"]):
        raise HTTPException(status_code=403, detail="Only the host can start the contest")

    if doc["status"] == "active":
        return {"success": True, "message": "Contest already active"}

    if doc["status"] != "lobby":
        raise HTTPException(status_code=400, detail="Contest has already started or finished")

    start_time = datetime.utcnow()
    end_time = start_time + timedelta(minutes=int(doc["duration_minutes"]))

    await db.contests.update_one(
        {"_id": doc["_id"]},
        {
            "$set": {
                "status": "active",
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            }
        }
    )

    # Broadcast started over WS
    room_key = doc.get("room_code") or doc.get("contest_id")
    await contest_ws_manager.broadcast(room_key, {
        "type": "contest_started",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    })

    return {"success": True, "message": "Contest started"}


@router.post("/{code_or_id}/cheating")
async def record_cheating_warning(
    code_or_id: str,
    payload: dict = Body(...),
    user_auth=Depends(UserMiddleware.me)
):
    user = user_auth["user"]
    event_type = payload.get("event_type")  # "tab_switch" | "focus_loss" | "copy_paste_attempt" | "fullscreen_exit"
    
    if not event_type:
        raise HTTPException(status_code=400, detail="Missing event_type")

    doc = await db.contests.find_one({
        "$or": [
            {"room_code": code_or_id.upper()},
            {"contest_id": code_or_id}
        ]
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Contest not found")

    participants = doc.get("participants", [])
    user_id_str = str(user["user_id"])
    updated = False
    disqualified = False
    warnings_count = 0

    for p in participants:
        if str(p.get("user_id")) == user_id_str:
            warnings = p.setdefault("warnings", [])
            warnings.append({
                "type": event_type,
                "timestamp": datetime.utcnow().isoformat()
            })
            warnings_count = len(warnings)
            
            # If warning count exceeds 3 (which means 4th warning triggers disqualification)
            if warnings_count > 3:
                p["disqualified"] = True
                disqualified = True
            
            updated = True
            break

    if not updated:
        raise HTTPException(status_code=400, detail="User is not a participant in this contest")

    await db.contests.update_one(
        {"_id": doc["_id"]},
        {"$set": {"participants": participants}}
    )

    # Broadcast updated warning state
    room_key = doc.get("room_code") or doc.get("contest_id")
    await contest_ws_manager.broadcast(room_key, {
        "type": "cheating_warning",
        "username": user["username"],
        "warnings_count": warnings_count,
        "disqualified": disqualified
    })

    return {
        "success": True,
        "warnings_count": warnings_count,
        "disqualified": disqualified
    }


@router.get("/{code_or_id}/leaderboard")
async def get_contest_leaderboard(code_or_id: str, user_auth=Depends(UserMiddleware.me)):
    doc = await db.contests.find_one({
        "$or": [
            {"room_code": code_or_id.upper()},
            {"contest_id": code_or_id}
        ]
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Contest not found")

    participants = doc.get("participants", [])
    
    # Sort descending for score, ascending for total runtime (optimization), then ascending for finish_time
    def sort_key(p):
        if p.get("disqualified", False):
            return (1, 9999999.0, "9999-12-31T23:59:59")
        score = p.get("total_score", 0)
        runtime = sum(s.get("runtime_ms", 0.0) for s in p.get("scores", {}).values() if s.get("solved"))
        f_time = p.get("finish_time") or "9999-12-31T23:59:59"
        return (-score, runtime, f_time)

    sorted_participants = sorted(participants, key=sort_key)

    # Map rank
    rank = 1
    rankings = []
    for p in sorted_participants:
        rankings.append({
            "rank": rank,
            "user_id": p.get("user_id"),
            "username": p.get("username"),
            "full_name": p.get("full_name"),
            "total_score": p.get("total_score", 0),
            "disqualified": p.get("disqualified", False),
            "finish_time": p.get("finish_time"),
            "warnings_count": len(p.get("warnings", [])),
            "scores": p.get("scores", {})
        })
        rank += 1

    return {"success": True, "data": rankings}


# ─── WebSocket Router ──────────────────────────────────────────────────────────

@router.websocket("/ws/{room_code}")
async def websocket_contest_room(websocket: WebSocket, room_code: str, token: Optional[str] = None):
    # Verify token
    user = None
    if not token:
        token = websocket.cookies.get("user")

    if token:
        payload = verify_token(token)
        if payload:
            user_id = payload.get("sub")
            user = await db.users.find_one({"user_id": user_id})

    if not user:
        # Accept and immediately close if unauthorized
        await websocket.accept()
        await websocket.close(code=4003, reason="Unauthorized")
        return

    # Check if contest exists
    contest = await db.contests.find_one({
        "$or": [
            {"room_code": room_code.upper()},
            {"contest_id": room_code}
        ]
    })
    if not contest:
        await websocket.accept()
        await websocket.close(code=4004, reason="Contest not found")
        return

    room_key = contest.get("room_code") or contest.get("contest_id")
    await contest_ws_manager.connect(room_key, websocket)

    # Broadcast initial message
    await contest_ws_manager.broadcast(room_key, {
        "type": "chat",
        "username": "System",
        "message": f"@{user['username']} joined the room.",
        "timestamp": datetime.utcnow().isoformat()
    })

    try:
        while True:
            # Wait for messages from client (e.g. Chat)
            data = await websocket.receive_text()
            try:
                msg_json = json.loads(data)
                if msg_json.get("type") == "chat":
                    text = msg_json.get("message")
                    if text:
                        await contest_ws_manager.broadcast(room_key, {
                            "type": "chat",
                            "username": user["username"],
                            "message": text,
                            "timestamp": datetime.utcnow().isoformat()
                        })
                elif msg_json.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except ValueError:
                pass  # Ignore invalid JSON
    except WebSocketDisconnect:
        await contest_ws_manager.disconnect(room_key, websocket)
        await contest_ws_manager.broadcast(room_key, {
            "type": "chat",
            "username": "System",
            "message": f"@{user['username']} left the room.",
            "timestamp": datetime.utcnow().isoformat()
        })
