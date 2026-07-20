# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any


class LangChainChatProvider:
    def __init__(
        self,
        *,
        provider: str,
        model: str,
        api_key: str | None,
        timeout: float,
        max_retries: int,
    ) -> None:
        self.name = provider
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Any | None = None

    def _build_client(self) -> Any:
        provider = self.name.lower()

        if provider == "openai":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                api_key=self.api_key,
                model=self.model,
                timeout=self.timeout,
                max_retries=self.max_retries,
            )

        if provider == "groq":
            from langchain_groq import ChatGroq

            return ChatGroq(
                api_key=self.api_key,
                model=self.model,
                timeout=self.timeout,
                max_retries=self.max_retries,
            )

        if provider in {"claude", "anthropic"}:
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                api_key=self.api_key,
                model=self.model,
                timeout=self.timeout,
                max_retries=self.max_retries,
            )

        if provider in {"gemini", "google"}:
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                google_api_key=self.api_key,
                model=self.model,
                timeout=self.timeout,
                max_retries=self.max_retries,
            )

        if provider == "ollama":
            from langchain_ollama import ChatOllama

            return ChatOllama(model=self.model)

        if provider == "deepseek":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                api_key=self.api_key,
                model=self.model,
                base_url="https://api.deepseek.com",
                timeout=self.timeout,
                max_retries=self.max_retries,
            )

        raise ValueError(f"Unsupported AI provider: {self.name}")

    @property
    def client(self) -> Any:
        if self._client is None:
            self._client = self._build_client()
        return self._client

    async def generate_text(
        self,
        *,
        system: str,
        user: str,
        temperature: float = 0.2,
    ) -> str:
        import asyncio
        runnable = self.client.bind(temperature=temperature)
        last_exc = None
        for attempt in range(3):
            try:
                response = await runnable.ainvoke([("system", system), ("human", user)])
                return str(response.content)
            except Exception as exc:
                last_exc = exc
                err_str = str(exc).lower()
                # If TPM (tokens per minute) burst rate limit (e.g. "try again in 780ms"), wait 1.2s and retry
                if ("rate_limit" in err_str or "429" in err_str or "tpm" in err_str) and "tpd" not in err_str and attempt < 2:
                    await asyncio.sleep(1.2 * (attempt + 1))
                    continue
                raise exc
        if last_exc:
            raise last_exc

    async def stream_text(
        self,
        *,
        system: str,
        user: str,
        temperature: float = 0.2,
    ) -> AsyncIterator[str]:
        runnable = self.client.bind(temperature=temperature)
        async for chunk in runnable.astream([("system", system), ("human", user)]):
            content = getattr(chunk, "content", "")
            if content:
                yield str(content)
