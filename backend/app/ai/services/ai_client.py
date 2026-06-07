from __future__ import annotations

import json
import os
from collections.abc import AsyncIterator
from typing import Any, TypeVar
import time

# Circuit breaker tracking for failed providers to avoid repeated latency on outages/limits
_failed_providers: dict[str, float] = {}
CIRCUIT_BREAKER_COOLDOWN_SECONDS = 180.0  # 3 minutes cooldown

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
        self._fallback_chain: list[LLMProvider] = []
        self._initialized_fallbacks = False

    def _get_fallback_chain(self) -> list[LLMProvider]:
        # Dynamically reload environment variables from .env to detect new keys without restarting Uvicorn
        try:
            from dotenv import load_dotenv
            load_dotenv(override=True)
        except Exception:
            pass

        import logging
        logger = logging.getLogger(__name__)

        chain = []
        # Add explicit fallback first if configured
        if self.fallback:
            chain.append(self.fallback)

        # Candidates for dynamic fallback
        candidates = [
            ("groq", "llama-3.3-70b-versatile"),
            ("openai", "gpt-4o-mini"),
            ("anthropic", "claude-3-5-sonnet-20241022"),
            ("google", "gemini-2.5-flash"),
            ("deepseek", "deepseek-chat"),
        ]

        # Prevent duplicates (don't add primary or explicit fallback again)
        already_added = {self.primary.name.lower()}
        if self.fallback:
            already_added.add(self.fallback.name.lower())

        for provider_name, default_model in candidates:
            if provider_name in already_added:
                continue
            
            # Check if key is in the env
            key = _api_key_for(provider_name)
            if key and key.strip():
                try:
                    p = LangChainChatProvider(
                        provider=provider_name,
                        model=default_model,
                        api_key=key,
                        timeout=AI_REQUEST_TIMEOUT_SECONDS,
                        max_retries=AI_MAX_RETRIES,
                    )
                    chain.append(p)
                    already_added.add(provider_name)
                except Exception as exc:
                    logger.warning(
                        f"[AIClient] Failed to instantiate dynamic fallback '{provider_name}': {exc}"
                    )

        return chain

    async def generate_text(
        self,
        *,
        system: str,
        user: str,
        temperature: float = 0.2,
    ) -> str:
        import logging
        logger = logging.getLogger(__name__)
        errors = []

        now = time.time()
        primary_name = self.primary.name.lower()

        # 1. Try primary provider (only if not tripped by circuit breaker)
        is_primary_tripped = False
        if primary_name in _failed_providers:
            elapsed = now - _failed_providers[primary_name]
            if elapsed < CIRCUIT_BREAKER_COOLDOWN_SECONDS:
                is_primary_tripped = True
                logger.info(
                    f"[AIClient] Skipping primary '{self.primary.name}' (Circuit Breaker active: "
                    f"failed {int(elapsed)}s ago, cooldown {int(CIRCUIT_BREAKER_COOLDOWN_SECONDS)}s)"
                )
                errors.append(f"Primary ({self.primary.name}): Skipped by Circuit Breaker")
            else:
                _failed_providers.pop(primary_name, None)

        if not is_primary_tripped:
            try:
                res = await self.primary.generate_text(
                    system=system,
                    user=user,
                    temperature=temperature,
                )
                _failed_providers.pop(primary_name, None)
                return res
            except Exception as exc:
                logger.warning(
                    f"[AIClient] Primary provider '{self.primary.name}' failed. "
                    f"Error: {exc}. Attempting fallback chain..."
                )
                _failed_providers[primary_name] = now
                errors.append(f"Primary ({self.primary.name}): {exc}")

        # 2. Try the fallback chain
        for fallback_provider in self._get_fallback_chain():
            fallback_name = fallback_provider.name.lower()
            if fallback_name in _failed_providers:
                elapsed = now - _failed_providers[fallback_name]
                if elapsed < CIRCUIT_BREAKER_COOLDOWN_SECONDS:
                    logger.info(
                        f"[AIClient] Skipping fallback '{fallback_provider.name}' (Circuit Breaker active)"
                    )
                    errors.append(f"Fallback ({fallback_provider.name}): Skipped by Circuit Breaker")
                    continue
                else:
                    _failed_providers.pop(fallback_name, None)

            try:
                res = await fallback_provider.generate_text(
                    system=system,
                    user=user,
                    temperature=temperature,
                )
                logger.info(
                    f"[AIClient] Fallback to provider '{fallback_provider.name}' succeeded."
                )
                _failed_providers.pop(fallback_name, None)
                return res
            except Exception as exc:
                logger.warning(
                    f"[AIClient] Fallback provider '{fallback_provider.name}' failed. "
                    f"Error: {exc}."
                )
                _failed_providers[fallback_name] = now
                errors.append(f"Fallback ({fallback_provider.name}): {exc}")

        raise RuntimeError(
            f"All AI providers in fallback chain failed. Errors: {'; '.join(errors)}"
        )

    async def stream_text(
        self,
        *,
        system: str,
        user: str,
        temperature: float = 0.2,
    ) -> AsyncIterator[str]:
        import logging
        logger = logging.getLogger(__name__)
        errors = []

        now = time.time()
        primary_name = self.primary.name.lower()

        # 1. Try primary provider
        is_primary_tripped = False
        if primary_name in _failed_providers:
            elapsed = now - _failed_providers[primary_name]
            if elapsed < CIRCUIT_BREAKER_COOLDOWN_SECONDS:
                is_primary_tripped = True
                logger.info(
                    f"[AIClient] Skipping primary '{self.primary.name}' in stream_text (Circuit Breaker active)"
                )
                errors.append(f"Primary ({self.primary.name}): Skipped by Circuit Breaker")
            else:
                _failed_providers.pop(primary_name, None)

        if not is_primary_tripped:
            try:
                async for token in self.primary.stream_text(
                    system=system,
                    user=user,
                    temperature=temperature,
                ):
                    yield token
                _failed_providers.pop(primary_name, None)
                return
            except Exception as exc:
                logger.warning(
                    f"[AIClient] Primary provider '{self.primary.name}' failed in stream_text. "
                    f"Error: {exc}. Attempting fallback chain..."
                )
                _failed_providers[primary_name] = now
                errors.append(f"Primary ({self.primary.name}): {exc}")

        # 2. Try the fallback chain
        for fallback_provider in self._get_fallback_chain():
            fallback_name = fallback_provider.name.lower()
            if fallback_name in _failed_providers:
                elapsed = now - _failed_providers[fallback_name]
                if elapsed < CIRCUIT_BREAKER_COOLDOWN_SECONDS:
                    logger.info(
                        f"[AIClient] Skipping fallback '{fallback_provider.name}' in stream_text (Circuit Breaker active)"
                    )
                    errors.append(f"Fallback ({fallback_provider.name}): Skipped by Circuit Breaker")
                    continue
                else:
                    _failed_providers.pop(fallback_name, None)

            try:
                async for token in fallback_provider.stream_text(
                    system=system,
                    user=user,
                    temperature=temperature,
                ):
                    yield token
                logger.info(
                    f"[AIClient] Fallback stream to provider '{fallback_provider.name}' succeeded."
                )
                _failed_providers.pop(fallback_name, None)
                return
            except Exception as exc:
                logger.warning(
                    f"[AIClient] Fallback provider '{fallback_provider.name}' failed in stream_text. "
                    f"Error: {exc}."
                )
                _failed_providers[fallback_name] = now
                errors.append(f"Fallback ({fallback_provider.name}): {exc}")

        raise RuntimeError(
            f"All AI providers in fallback chain failed during stream_text. Errors: {'; '.join(errors)}"
        )

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
    prov = provider.lower()
    if prov == "openai":
        return os.getenv("OPENAI_API_KEY") or OPENAI_API_KEY
    if prov in {"claude", "anthropic"}:
        return os.getenv("ANTHROPIC_API_KEY") or ANTHROPIC_API_KEY
    if prov in {"gemini", "google"}:
        return os.getenv("GOOGLE_API_KEY") or GOOGLE_API_KEY
    if prov == "groq":
        return os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if prov == "deepseek":
        return os.getenv("DEEPSEEK_API_KEY") or DEEPSEEK_API_KEY
    return None


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

