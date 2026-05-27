from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from app.ai.providers.base import LLMProvider
from app.ai.providers.langchain_provider import LangChainChatProvider
from app.core.config import (
    AI_FALLBACK_MODEL,
    AI_FALLBACK_PROVIDER,
    AI_MAX_RETRIES,
    AI_MODEL,
    AI_PROVIDER,
    AI_REQUEST_TIMEOUT_SECONDS,
    ANTHROPIC_API_KEY,
    DEEPSEEK_API_KEY,
    GOOGLE_API_KEY,
    GROQ_API_KEY,
    OPENAI_API_KEY,
)

T = TypeVar("T", bound=BaseModel)


class AIClient:
    def __init__(
        self,
        *,
        primary: LLMProvider,
        fallback: LLMProvider | None = None,
    ) -> None:
        self.primary = primary
        self.fallback = fallback

    async def generate_text(
        self,
        *,
        system: str,
        user: str,
        temperature: float = 0.2,
    ) -> str:
        try:
            return await self.primary.generate_text(
                system=system,
                user=user,
                temperature=temperature,
            )
        except Exception:
            if self.fallback is None:
                raise
            return await self.fallback.generate_text(
                system=system,
                user=user,
                temperature=temperature,
            )

    async def stream_text(
        self,
        *,
        system: str,
        user: str,
        temperature: float = 0.2,
    ) -> AsyncIterator[str]:
        provider = self.primary
        try:
            async for token in provider.stream_text(
                system=system,
                user=user,
                temperature=temperature,
            ):
                yield token
        except Exception:
            if self.fallback is None:
                raise
            async for token in self.fallback.stream_text(
                system=system,
                user=user,
                temperature=temperature,
            ):
                yield token

    async def generate_json(
        self,
        *,
        system: str,
        user: str,
        schema: type[T],
        temperature: float = 0.2,
    ) -> T:
        raw = await self.generate_text(
            system=system,
            user=f"{user}\n\nReturn valid JSON only. Do not include markdown.",
            temperature=temperature,
        )
        payload = _extract_json(raw)
        try:
            return schema.model_validate(payload)
        except ValidationError as exc:
            repair_prompt = (
                "The previous model output did not match the required schema. "
                f"Schema: {schema.model_json_schema()}\n"
                f"Invalid output: {raw}\n"
                f"Validation error: {exc}\n"
                "Return corrected JSON only."
            )
            repaired = await self.generate_text(
                system=system,
                user=repair_prompt,
                temperature=0,
            )
            return schema.model_validate(_extract_json(repaired))


def _extract_json(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"LLM response did not contain a JSON object: {raw}")
    return json.loads(text[start : end + 1])


def _api_key_for(provider: str) -> str | None:
    return {
        "openai": OPENAI_API_KEY,
        "claude": ANTHROPIC_API_KEY,
        "anthropic": ANTHROPIC_API_KEY,
        "gemini": GOOGLE_API_KEY,
        "google": GOOGLE_API_KEY,
        "groq": GROQ_API_KEY,
        "deepseek": DEEPSEEK_API_KEY,
        "ollama": None,
    }.get(provider.lower())


def build_ai_client() -> AIClient:
    primary = LangChainChatProvider(
        provider=AI_PROVIDER,
        model=AI_MODEL,
        api_key=_api_key_for(AI_PROVIDER),
        timeout=AI_REQUEST_TIMEOUT_SECONDS,
        max_retries=AI_MAX_RETRIES,
    )
    fallback = None
    if AI_FALLBACK_PROVIDER and AI_FALLBACK_MODEL:
        fallback = LangChainChatProvider(
            provider=AI_FALLBACK_PROVIDER,
            model=AI_FALLBACK_MODEL,
            api_key=_api_key_for(AI_FALLBACK_PROVIDER),
            timeout=AI_REQUEST_TIMEOUT_SECONDS,
            max_retries=AI_MAX_RETRIES,
        )
    return AIClient(primary=primary, fallback=fallback)


ai_client = build_ai_client()
