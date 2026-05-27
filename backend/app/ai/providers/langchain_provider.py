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
        runnable = self.client.bind(temperature=temperature)
        response = await runnable.ainvoke([("system", system), ("human", user)])
        return str(response.content)

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
