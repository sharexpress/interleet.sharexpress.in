"""
Interleet Challenge Validation — Base Mutant Strategy
Abstract base class for all mutant generators.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MutantStrategy(ABC):
    """
    A mutant strategy generates intentionally-wrong code that should FAIL
    all hidden tests. If a mutant PASSES, the challenge's test coverage
    is insufficient.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name for this mutant type."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """What kind of cheating this mutant simulates."""
        ...

    @abstractmethod
    def generate(
        self,
        language: str,
        sample_test_cases: list[dict[str, Any]],
    ) -> str:
        """
        Generate mutant source code for the given language.

        Args:
            language: Target language (python, javascript, etc.)
            sample_test_cases: Visible sample test cases with stdin/expected_output.

        Returns:
            Source code string of the intentionally-wrong solution.
        """
        ...

    @property
    def supported_languages(self) -> list[str]:
        """Languages this mutant can generate code for. Override to restrict."""
        return ["python", "javascript", "typescript", "go", "cpp", "rust", "java"]
