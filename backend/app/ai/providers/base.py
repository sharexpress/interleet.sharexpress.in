from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Protocol


class LLMProvider(Protocol):
    name: str

    async def generate_text(
        self,
        *,
        system: str,
        user: str,
        temperature: float = 0.2,
    ) -> str:
        ...

    async def stream_text(
        self,
        *,
        system: str,
        user: str,
        temperature: float = 0.2,
    ) -> AsyncIterator[str]:
        ...
