"""
Interleet Challenge Validation — Differential Tester
Compares a candidate solution against a reference solution on generated inputs.
Particularly useful for parsers, interpreters, data structures, and system simulations.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class DiffMismatch:
    """A single mismatch between candidate and reference output."""

    def __init__(
        self,
        seed: int,
        stdin: str,
        candidate_output: str,
        reference_output: str,
    ):
        self.seed = seed
        self.stdin = stdin
        self.candidate_output = candidate_output
        self.reference_output = reference_output

    def to_dict(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            "stdin": self.stdin[:500],  # Truncate for readability
            "candidate_output": self.candidate_output[:500],
            "reference_output": self.reference_output[:500],
        }


class DiffReport:
    """Result of differential testing."""

    def __init__(
        self,
        total_cases: int,
        matches: int,
        mismatches: list[DiffMismatch],
        match_rate: float,
        passed: bool,
    ):
        self.total_cases = total_cases
        self.matches = matches
        self.mismatches = mismatches
        self.match_rate = match_rate
        self.passed = passed

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_cases": self.total_cases,
            "matches": self.matches,
            "mismatch_count": len(self.mismatches),
            "match_rate": self.match_rate,
            "passed": self.passed,
            "mismatches": [m.to_dict() for m in self.mismatches[:10]],  # First 10
        }


class DifferentialTester:
    """
    Run a candidate solution and a reference solution against the same
    generated inputs, then compare their outputs.
    """

    async def compare(
        self,
        candidate_code: str,
        candidate_language: str,
        reference_code: str,
        reference_language: str,
        generator_code: str,
        sample_count: int = 20,
    ) -> DiffReport:
        """
        Generate random inputs, run both solutions, and compare outputs.

        Args:
            candidate_code: The submitted solution.
            candidate_language: Language of the candidate.
            reference_code: The canonical reference solution.
            reference_language: Language of the reference.
            generator_code: Python code defining generate_test_case(seed) -> str.
            sample_count: Number of random inputs to test.

        Returns:
            DiffReport with match rate and any mismatches.
        """
        from app.engine.validation.test_generator import TestGenerator

        generator = TestGenerator()
        mismatches: list[DiffMismatch] = []
        matches = 0
        total = 0

        for seed in range(1, sample_count + 1):
            try:
                # Generate input
                stdin = await generator._run_generator(generator_code, seed)
                if stdin is None:
                    continue

                # Run reference
                ref_output = await generator._run_reference(
                    reference_code, reference_language, stdin,
                )
                if ref_output is None:
                    continue

                # Run candidate
                cand_output = await generator._run_reference(
                    candidate_code, candidate_language, stdin,
                )
                if cand_output is None:
                    cand_output = ""

                total += 1

                # Compare (trimmed)
                if ref_output.strip() == cand_output.strip():
                    matches += 1
                else:
                    mismatches.append(DiffMismatch(
                        seed=seed,
                        stdin=stdin,
                        candidate_output=cand_output,
                        reference_output=ref_output,
                    ))

            except Exception as exc:
                logger.exception("Differential test failed for seed=%d: %s", seed, exc)
                continue

        match_rate = round((matches / total) * 100, 2) if total > 0 else 0.0
        passed = (matches == total) and total > 0

        logger.info(
            "Differential testing: %d/%d matches (%.1f%%), passed=%s",
            matches, total, match_rate, passed,
        )

        return DiffReport(
            total_cases=total,
            matches=matches,
            mismatches=mismatches,
            match_rate=match_rate,
            passed=passed,
        )
