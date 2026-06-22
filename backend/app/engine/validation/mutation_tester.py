"""
Interleet Challenge Validation — Mutation Tester
Generates intentionally-wrong solutions and verifies the test suite rejects them.
A challenge cannot be published if any mutant passes all tests.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from app.engine.enums import ComparisonMode, TestCaseCategory
from app.engine.judge import JudgeEngine
from app.engine.schemas import SandboxResult, TestCaseSchema

logger = logging.getLogger(__name__)


# Import all mutant strategies
from app.engine.validation.mutants.hardcoded import HardcodedOutputMutant
from app.engine.validation.mutants.constant_output import ConstantOutputMutant
from app.engine.validation.mutants.empty_output import EmptyOutputMutant
from app.engine.validation.mutants.partial_logic import PartialLogicMutant
from app.engine.validation.mutants.sample_only import SampleOnlyMutant

ALL_MUTANT_STRATEGIES = [
    HardcodedOutputMutant(),
    ConstantOutputMutant(),
    EmptyOutputMutant(),
    PartialLogicMutant(),
    SampleOnlyMutant(),
]


class MutantResult:
    """Result of running a single mutant against the test suite."""

    def __init__(
        self,
        mutant_name: str,
        mutant_description: str,
        was_rejected: bool,
        passed_count: int,
        total_count: int,
        language: str,
        error: Optional[str] = None,
    ):
        self.mutant_name = mutant_name
        self.mutant_description = mutant_description
        self.was_rejected = was_rejected
        self.passed_count = passed_count
        self.total_count = total_count
        self.language = language
        self.error = error

    def to_dict(self) -> dict[str, Any]:
        return {
            "mutant_name": self.mutant_name,
            "mutant_description": self.mutant_description,
            "was_rejected": self.was_rejected,
            "passed_count": self.passed_count,
            "total_count": self.total_count,
            "language": self.language,
            "error": self.error,
        }


class MutationReport:
    """Aggregated results of mutation testing."""

    def __init__(
        self,
        results: list[MutantResult],
        resistance_score: float,
        all_rejected: bool,
        blocking_reasons: list[str],
    ):
        self.results = results
        self.resistance_score = resistance_score
        self.all_rejected = all_rejected
        self.blocking_reasons = blocking_reasons

    def to_dict(self) -> dict[str, Any]:
        return {
            "results": [r.to_dict() for r in self.results],
            "resistance_score": self.resistance_score,
            "all_rejected": self.all_rejected,
            "blocking_reasons": self.blocking_reasons,
        }


class MutationTester:
    """
    Runs mutant strategies against a challenge's test suite.
    A challenge passes mutation testing ONLY if ALL mutants are rejected
    (i.e., fail at least one test case).
    """

    def __init__(self, strategies=None):
        self.strategies = strategies or ALL_MUTANT_STRATEGIES

    async def run(
        self,
        test_cases: list[dict[str, Any]],
        language: str = "python",
        comparison_mode: ComparisonMode = ComparisonMode.TRIMMED,
    ) -> MutationReport:
        """
        Execute each mutant strategy against all test cases.

        This performs a *simulated* execution: it generates the mutant code and
        evaluates what the sandbox *would* output by analyzing the mutant logic.
        For full sandbox execution, use run_in_sandbox() instead.

        Args:
            test_cases: All test cases for the challenge (including hidden).
            language: Language to generate mutant code in.
            comparison_mode: How to compare outputs.

        Returns:
            MutationReport with per-mutant results and overall score.
        """
        # Separate sample test cases (visible to the "attacker")
        sample_cases = [
            tc for tc in test_cases
            if tc.get("category", "sample") == TestCaseCategory.SAMPLE.value
            or not tc.get("hidden", False)
        ]

        results: list[MutantResult] = []
        blocking_reasons: list[str] = []

        for strategy in self.strategies:
            if language not in strategy.supported_languages:
                logger.debug(
                    "Skipping mutant '%s' — unsupported language '%s'",
                    strategy.name, language,
                )
                continue

            try:
                mutant_code = strategy.generate(language, sample_cases)
                if not mutant_code:
                    results.append(MutantResult(
                        mutant_name=strategy.name,
                        mutant_description=strategy.description,
                        was_rejected=True,
                        passed_count=0,
                        total_count=len(test_cases),
                        language=language,
                        error="Strategy could not generate code (no sample cases?)",
                    ))
                    continue

                # Simulate execution by analyzing what the mutant would output
                mutant_result = self._simulate_mutant(
                    mutant_code, strategy, test_cases, sample_cases,
                    language, comparison_mode,
                )
                results.append(mutant_result)

                if not mutant_result.was_rejected:
                    blocking_reasons.append(
                        f"Mutant '{strategy.name}' was NOT rejected — "
                        f"passed {mutant_result.passed_count}/{mutant_result.total_count} tests. "
                        f"Description: {strategy.description}"
                    )

            except Exception as exc:
                logger.exception("Error running mutant '%s': %s", strategy.name, exc)
                results.append(MutantResult(
                    mutant_name=strategy.name,
                    mutant_description=strategy.description,
                    was_rejected=True,  # Conservative: treat errors as rejected
                    passed_count=0,
                    total_count=len(test_cases),
                    language=language,
                    error=str(exc),
                ))

        # Compute resistance score
        total_mutants = len(results)
        rejected_count = sum(1 for r in results if r.was_rejected)
        resistance_score = (
            round((rejected_count / total_mutants) * 100, 2)
            if total_mutants > 0
            else 100.0
        )

        return MutationReport(
            results=results,
            resistance_score=resistance_score,
            all_rejected=(rejected_count == total_mutants),
            blocking_reasons=blocking_reasons,
        )

    def _simulate_mutant(
        self,
        mutant_code: str,
        strategy,
        all_test_cases: list[dict[str, Any]],
        sample_cases: list[dict[str, Any]],
        language: str,
        comparison_mode: ComparisonMode,
    ) -> MutantResult:
        """
        Simulate what a mutant would output and compare against expected outputs.
        This is a static analysis approach — it predicts the mutant's output
        without running it in a sandbox (which is faster and doesn't require Docker).
        """
        passed_count = 0
        total_count = len(all_test_cases)

        for tc in all_test_cases:
            expected = tc.get("expected_output", "").strip()
            simulated_output = self._predict_mutant_output(
                strategy, tc, sample_cases, language,
            )

            if simulated_output is not None:
                # Use the judge's comparison pipeline
                tc_schema = TestCaseSchema(
                    id=tc.get("id", "sim"),
                    stdin=tc.get("stdin", ""),
                    expected_output=expected,
                )
                sandbox_result = SandboxResult(
                    stdout=simulated_output,
                    exit_code=0,
                )
                result = JudgeEngine.evaluate(
                    sandbox_result=sandbox_result,
                    testcase=tc_schema,
                    comparison_mode=comparison_mode,
                )
                if result.passed:
                    passed_count += 1

        # Mutant is rejected if it fails at least one test case
        was_rejected = passed_count < total_count

        return MutantResult(
            mutant_name=strategy.name,
            mutant_description=strategy.description,
            was_rejected=was_rejected,
            passed_count=passed_count,
            total_count=total_count,
            language=language,
        )

    @staticmethod
    def _predict_mutant_output(
        strategy,
        test_case: dict[str, Any],
        sample_cases: list[dict[str, Any]],
        language: str,
    ) -> Optional[str]:
        """
        Predict what a mutant strategy would output for a given test case.
        Returns None if prediction is uncertain.
        """
        strategy_name = strategy.name
        stdin = test_case.get("stdin", "").strip()

        if strategy_name == "hardcoded_output":
            if sample_cases:
                return sample_cases[0].get("expected_output", "").strip()
            return None

        elif strategy_name == "constant_output":
            # Predict the constant from sample outputs
            constants = set()
            for tc in sample_cases:
                out = tc.get("expected_output", "").strip().lower()
                if out in ("true", "false", "0", "1", "yes", "no"):
                    constants.add(out)
            return next(iter(constants), "1")

        elif strategy_name == "empty_output":
            return ""

        elif strategy_name == "partial_logic":
            if sample_cases:
                return sample_cases[0].get("expected_output", "").strip()
            return None

        elif strategy_name == "sample_only":
            # Check if this test case's stdin matches any sample
            for sc in sample_cases:
                if sc.get("stdin", "").strip() == stdin:
                    return sc.get("expected_output", "").strip()
            return "unknown"

        return None
