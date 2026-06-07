from fastapi import APIRouter, Body, Query, Depends

from app.controllers.platform import PlatformController
from app.middleware.user import Middleware as UserMiddleware

router = APIRouter(prefix="/api", tags=["Platform"])


@router.get("/dashboard")
async def dashboard():
    return await PlatformController.dashboard()


@router.get("/challenges")
async def list_challenges(
    q: str | None = None,
    domain: str | None = None,
    difficulty: str | None = None,
    sort: str = Query(default="popular"),
):
    return await PlatformController.list_challenges(q=q, domain=domain, difficulty=difficulty, sort=sort)


@router.post("/challenges")
async def create_challenge(payload: dict = Body(...)):
    return await PlatformController.create_challenge(payload)


@router.get("/challenges/{slug}")
async def get_challenge(slug: str):
    return await PlatformController.get_challenge(slug)


@router.get("/leaderboard")
async def leaderboard(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    q: str | None = None,
):
    return await PlatformController.leaderboard(page=page, limit=limit, q=q)


@router.get("/profile")
async def my_profile(user=Depends(UserMiddleware.me)):
    return await PlatformController.profile(username=user["user"]["username"])


@router.get("/profile/{username}")
async def profile(username: str):
    return await PlatformController.profile(username=username)


@router.get("/profile/{username}/ai-evaluation")
async def profile_ai_evaluation(username: str, force: bool = False):
    return await PlatformController.ai_evaluation(username=username, force_refresh=force)


@router.get("/activity")
async def activity():
    return await PlatformController.activity()


@router.get("/interviews")
async def interviews():
    return await PlatformController.interviews()


@router.get("/system-design")
async def system_design():
    return await PlatformController.system_design()


@router.get("/candidates")
async def candidates():
    return await PlatformController.candidates()
