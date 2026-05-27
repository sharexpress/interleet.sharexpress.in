from __future__ import annotations

import json
from typing import Any

from app.core.config import INTERVIEW_SESSION_TTL_SECONDS

try:
    from app.lib.redis import Redis_client
except Exception:
    Redis_client = None


class SessionService:
    _memory: dict[str, dict[str, Any]] = {}

    @classmethod
    async def create_session(cls, session_id: str, state: dict[str, Any]) -> None:
        await cls.update_session(session_id, state)

    @classmethod
    async def get_session(cls, session_id: str) -> dict[str, Any] | None:
        key = cls._key(session_id)
        if Redis_client is not None:
            try:
                cached = Redis_client.get(key)
                if cached:
                    return json.loads(cached)
            except Exception:
                pass
        return cls._memory.get(session_id)

    @classmethod
    async def update_session(cls, session_id: str, state: dict[str, Any]) -> None:
        cls._memory[session_id] = state
        if Redis_client is not None:
            try:
                Redis_client.setex(
                    cls._key(session_id),
                    INTERVIEW_SESSION_TTL_SECONDS,
                    json.dumps(state),
                )
            except Exception:
                pass

    @classmethod
    async def delete_session(cls, session_id: str) -> None:
        cls._memory.pop(session_id, None)
        if Redis_client is not None:
            try:
                Redis_client.delete(cls._key(session_id))
            except Exception:
                pass

    @staticmethod
    def _key(session_id: str) -> str:
        return f"interview:session:{session_id}"
