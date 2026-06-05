from fastapi import APIRouter, Body, Query, Depends
from typing import Optional

from app.controllers.challenge import ChallengeController
from app.middleware.user import Middleware as UserMiddleware

router = APIRouter(prefix="/challenges", tags=["Challenges"])


@router.get("")
async def list_challenges(
    q: Optional[str] = Query(default=None, description="Search title, tags, summary"),
    domain: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
    sort: str = Query(
        default="popular", description="popular | xp | time | completion"
    ),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=100),
):
    return await ChallengeController.list_challenges(
        q=q, domain=domain, difficulty=difficulty, sort=sort, page=page, limit=limit
    )


@router.get("/{slug}")
async def get_challenge(slug: str):
    return await ChallengeController.get_challenge(slug)


@router.post("/create")
async def create_challenge(
    payload: dict = Body(...),
):
    return await ChallengeController.create_challenge(payload)


@router.patch("/{slug}")
async def update_challenge(
    slug: str,
    payload: dict = Body(...),
    _user=Depends(UserMiddleware.me),
):
    return await ChallengeController.update_challenge(slug, payload)


@router.delete("/{slug}")
async def delete_challenge(
    slug: str,
    _user=Depends(UserMiddleware.me),
):
    return await ChallengeController.delete_challenge(slug)


@router.post("/{slug}/featured")
async def toggle_featured(
    slug: str,
    _user=Depends(UserMiddleware.me),
):
    return await ChallengeController.toggle_featured(slug)


@router.post("/{slug}/publish")
async def toggle_publish(
    slug: str,
    _user=Depends(UserMiddleware.me),
):
    return await ChallengeController.toggle_publish(slug)
