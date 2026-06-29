from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from datetime import datetime
from uuid import uuid4

from app.middleware.user import Middleware as UserMiddleware
from app.core.db import get_db
from app.models.notifications import NotificationModel
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])
db = get_db()


@router.get("")
async def list_notifications(user_auth=Depends(UserMiddleware.me)):
    user_id = str(user_auth["user"]["user_id"])
    cursor = db.notifications.find({"user_id": user_id}).sort("created_at", -1)
    notifications = []
    async for doc in cursor:
        doc.pop("_id", None)
        notifications.append(doc)
    return {"success": True, "data": notifications}


@router.post("/{notification_id}/read")
async def mark_read(notification_id: str, user_auth=Depends(UserMiddleware.me)):
    user_id = str(user_auth["user"]["user_id"])
    res = await db.notifications.update_one(
        {"id": notification_id, "user_id": user_id},
        {"$set": {"read": True}},
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"success": True, "message": "Notification marked as read"}


@router.post("/read-all")
async def mark_all_read(user_auth=Depends(UserMiddleware.me)):
    user_id = str(user_auth["user"]["user_id"])
    await db.notifications.update_many(
        {"user_id": user_id, "read": False},
        {"$set": {"read": True}},
    )
    return {"success": True, "message": "All notifications marked as read"}


@router.post("/invite")
async def invite_user(
    payload: dict = Body(...),
    user_auth=Depends(UserMiddleware.me),
):
    """
    Invite a user to a contest room.
    Sends them an in-app notification.
    """
    inviter = user_auth["user"]
    target_username = payload.get("username")
    room_code = payload.get("room_code")
    contest_title = payload.get("contest_title", "Coding Contest")

    if not target_username or not room_code:
        raise HTTPException(status_code=400, detail="Missing username or room_code")

    # Find target user
    target_user = await db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    target_user_id = str(target_user["user_id"])

    notification = NotificationModel(
        user_id=target_user_id,
        title="Contest Invitation",
        message=f"{inviter.get('full_name') or inviter['username']} invited you to join the contest room {room_code} ({contest_title}).",
        type="invite",
        link=f"/app/contest/room/{room_code}",
        read=False,
    )

    doc = notification.dict()
    await db.notifications.insert_one(doc)

    return {"success": True, "message": f"Invitation sent to @{target_username}"}


@router.get("/unread-count")
async def unread_count(user_auth=Depends(UserMiddleware.me)):
    """Get count of unread notifications for the notification bell badge."""
    user_id = str(user_auth["user"]["user_id"])
    count = await NotificationService.get_unread_count(user_id)
    return {"success": True, "count": count}


@router.delete("/{notification_id}")
async def delete_notification(notification_id: str, user_auth=Depends(UserMiddleware.me)):
    """Delete a specific notification."""
    user_id = str(user_auth["user"]["user_id"])
    res = await db.notifications.delete_one(
        {"id": notification_id, "user_id": user_id}
    )
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"success": True, "message": "Notification deleted"}


@router.post("/generate")
async def generate_daily(user_auth=Depends(UserMiddleware.me)):
    """Trigger daily notification generation for the current user."""
    user_id = str(user_auth["user"]["user_id"])
    notifications = await NotificationService.generate_daily_notifications(user_id)
    return {
        "success": True,
        "generated": len(notifications),
        "notifications": [{"title": n["title"], "message": n["message"]} for n in notifications],
    }
