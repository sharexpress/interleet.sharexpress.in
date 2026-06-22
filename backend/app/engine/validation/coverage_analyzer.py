"""
Interleet Challenge Validation — Coverage Analyzer
Analyzes test case distribution across categories and enforces minimum coverage.
"""

from __future__ import annotations

import logging
from collections import Counter
from typing import Any

from app.engine.enums import TestCaseCategory

logger = logging.getLogger(__name__)


# Minimum test case counts per category for a challenge to pass the quality gate.
# These are intentionally set as a baseline — individual challenges may need more.
MINIMUM_REQUIREMENTS: dict[str, int] = {
    TestCaseCategory.SAMPLE.value: 1,
    TestCaseCategory.FUNCTIONAL.value: 5,
    TestCaseCategory.EDGE_CASE.value: 3,
    TestCaseCategory.ADVERSARIAL.value: 3,
    TestCaseCategory.RANDOMIZED.value: 10,
}


class CoverageReport:
    """Result of coverage analysis."""

    def __init__(
        self,
        test_counts: dict[str, int],
        minimum_requirements: dict[str, int],
        deficiencies: dict[str, int],
        score: float,
        passed: bool,
        blocking_reasons: list[str],
    ):
        self.test_counts = test_counts
        self.minimum_requirements = minimum_requirements
        self.deficiencies = deficiencies
        self.score = score
        self.passed = passed
        self.blocking_reasons = blocking_reasons

    def to_dict(self) -> dict[str, Any]:
        return {
            "test_counts": self.test_counts,
            "minimum_requirements": self.minimum_requirements,
            "deficiencies": self.deficiencies,
            "score": self.score,
            "passed": self.passed,
            "blocking_reasons": self.blocking_reasons,
        }


class CoverageAnalyzer:
    """Analyzes test case distribution and enforces minimum coverage requirements."""

    @staticmethod
    def analyze(
        test_cases: list[dict[str, Any]],
        requirements: dict[str, int] | None = None,
    ) -> CoverageReport:
        """
        Count test cases by category, check against minimums, return a CoverageReport.

        Args:
            test_cases: List of test case dicts, each with a 'category' field.
            requirements: Override minimum requirements (default: MINIMUM_REQUIREMENTS).

        Returns:
            CoverageReport with score, deficiencies, and pass/fail status.
        """
        reqs = requirements or MINIMUM_REQUIREMENTS

        # Count test cases by category
        counts = Counter(
            tc.get("category", TestCaseCategory.SAMPLE.value)
            for tc in test_cases
        )

        # Ensure all required categories appear in counts
        for category in reqs:
            if category not in counts:
                counts[category] = 0

        # Compute deficiencies (how many more test cases are needed)
        deficiencies: dict[str, int] = {}
        blocking_reasons: list[str] = []

        for category, minimum in reqs.items():
            actual = counts.get(category, 0)
            if actual < minimum:
                shortfall = minimum - actual
                deficiencies[category] = shortfall
                blocking_reasons.append(
                    f"Category '{category}' has {actual}/{minimum} test cases "
                    f"(need {shortfall} more)"
                )

        # Compute weighted score (0–100)
        score = CoverageAnalyzer._compute_score(dict(counts), reqs)
        passed = len(deficiencies) == 0

        logger.info(
            "Coverage analysis: score=%.1f%% passed=%s categories=%s deficiencies=%s",
            score, passed, dict(counts), deficiencies,
        )

        return CoverageReport(
            test_counts=dict(counts),
            minimum_requirements=reqs,
            deficiencies=deficiencies,
            score=score,
            passed=passed,
            blocking_reasons=blocking_reasons,
        )

    @staticmethod
    def _compute_score(counts: dict[str, int], requirements: dict[str, int]) -> float:
        """
        Weighted coverage percentage.
        Each category contributes equally. A category scores min(actual/required, 1.0).
        """
        if not requirements:
            return 100.0

        total_score = 0.0
        for category, minimum in requirements.items():
            actual = counts.get(category, 0)
            if minimum > 0:
                total_score += min(actual / minimum, 1.0)
            else:
                total_score += 1.0  # No requirement = automatically met

        return round((total_score / len(requirements)) * 100, 2)
