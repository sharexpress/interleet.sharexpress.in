"""
Interleet Challenge Validation — Quality Gate
Orchestrates all validation checks and produces a pass/fail decision.
This is the central gatekeeper that blocks challenge publishing if quality
requirements are not met.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from app.core.db import get_db
from app.engine.enums import ComparisonMode
from app.engine.validation.coverage_analyzer import CoverageAnalyzer
from app.engine.validation.mutation_tester import MutationTester
from app.models.validation_report import ValidationReport

logger = logging.getLogger(__name__)


# Configurable thresholds — a challenge must meet ALL of these
QUALITY_THRESHOLDS = {
    "coverage_score": 90.0,       # Minimum coverage score (0–100)
    "mutation_resistance": 100.0, # All mutants must be rejected
    "edge_case_required": True,   # Edge case category must meet minimums
}


class QualityGate:
    """
    Runs all validation checks on a challenge and returns a ValidationReport.

    Checks performed:
    1. Coverage Analysis — Are all test case categories sufficiently populated?
    2. Mutation Testing — Do intentionally-wrong solutions get rejected?
    3. Edge Case Coverage — Are edge cases explicitly covered?

    A challenge must pass ALL checks to be publishable.
    """

    def __init__(self, thresholds: dict | None = None):
        self.thresholds = thresholds or QUALITY_THRESHOLDS

    async def evaluate(
        self,
        challenge_slug: str,
        admin_user_id: Optional[str] = None,
    ) -> ValidationReport:
        """
        Run the full quality gate on a challenge.

        Args:
            challenge_slug: The slug of the challenge to evaluate.
            admin_user_id: The admin running the evaluation.

        Returns:
            ValidationReport with pass/fail and detailed breakdown.
        """
        db = get_db()
        blocking_reasons: list[str] = []

        # ── Fetch challenge and test cases ─────────────────────────────
        challenge = await db.problems.find_one({"slug": challenge_slug})
        if not challenge:
            return ValidationReport(
                challenge_slug=challenge_slug,
                passed=False,
                blocking_reasons=[f"Challenge '{challenge_slug}' not found"],
                created_by=admin_user_id,
            )

        # Get test cases from embedded array or separate collection
        test_cases = await self._get_all_test_cases(challenge_slug, challenge)
        if not test_cases:
            return ValidationReport(
                challenge_slug=challenge_slug,
                passed=False,
                blocking_reasons=["Challenge has no test cases"],
                created_by=admin_user_id,
            )

        logger.info(
            "Running quality gate for '%s' with %d test cases",
            challenge_slug, len(test_cases),
        )

        # ── Check 1: Coverage Analysis ─────────────────────────────────
        coverage_report = CoverageAnalyzer.analyze(test_cases)
        if not coverage_report.passed:
            blocking_reasons.extend(coverage_report.blocking_reasons)

        # ── Check 2: Mutation Testing ──────────────────────────────────
        mutation_tester = MutationTester()

        # Determine the primary language for mutation testing
        language = self._detect_language(challenge)

        mutation_report = await mutation_tester.run(
            test_cases=test_cases,
            language=language,
            comparison_mode=ComparisonMode.TRIMMED,
        )
        if not mutation_report.all_rejected:
            blocking_reasons.extend(mutation_report.blocking_reasons)

        # ── Check 3: Edge Case Coverage ────────────────────────────────
        edge_cases = [
            tc for tc in test_cases
            if tc.get("category") == "edge_case"
        ]
        edge_case_passed = len(edge_cases) >= 3  # Minimum 3 edge cases
        if not edge_case_passed and self.thresholds.get("edge_case_required", True):
            blocking_reasons.append(
                f"Edge case coverage insufficient: {len(edge_cases)}/3 edge case tests"
            )

        # ── Aggregate Results ──────────────────────────────────────────
        coverage_threshold = self.thresholds.get("coverage_score", 90.0)
        mutation_threshold = self.thresholds.get("mutation_resistance", 100.0)

        score_check = coverage_report.score >= coverage_threshold
        mutation_check = mutation_report.resistance_score >= mutation_threshold

        if not score_check:
            blocking_reasons.append(
                f"Coverage score {coverage_report.score}% is below "
                f"threshold {coverage_threshold}%"
            )
        if not mutation_check:
            blocking_reasons.append(
                f"Mutation resistance {mutation_report.resistance_score}% is below "
                f"threshold {mutation_threshold}%"
            )

        passed = len(blocking_reasons) == 0

        report = ValidationReport(
            id=str(uuid4()),
            challenge_slug=challenge_slug,
            coverage_score=coverage_report.score,
            mutation_resistance=mutation_report.resistance_score,
            edge_case_coverage="PASS" if edge_case_passed else "FAIL",
            test_counts=coverage_report.test_counts,
            minimum_requirements=coverage_report.minimum_requirements,
            category_deficiencies=coverage_report.deficiencies,
            mutant_results=[r.to_dict() for r in mutation_report.results],
            passed=passed,
            blocking_reasons=blocking_reasons,
            created_at=datetime.utcnow(),
            created_by=admin_user_id,
        )

        logger.info(
            "Quality gate result for '%s': passed=%s coverage=%.1f%% "
            "mutation_resistance=%.1f%% edge_cases=%s reasons=%d",
            challenge_slug, passed, coverage_report.score,
            mutation_report.resistance_score,
            "PASS" if edge_case_passed else "FAIL",
            len(blocking_reasons),
        )

        return report

    async def _get_all_test_cases(
        self, slug: str, challenge: dict,
    ) -> list[dict[str, Any]]:
        """
        Get all test cases for a challenge, from embedded array and/or
        separate test_cases collection.
        """
        db = get_db()
        test_cases: list[dict[str, Any]] = []

        # From embedded array in challenge doc
        embedded = challenge.get("test_cases", [])
        for tc in embedded:
            if isinstance(tc, dict):
                test_cases.append(tc)

        # From separate test_cases collection
        cursor = db.test_cases.find({"problem_slug": slug})
        async for tc_doc in cursor:
            tc_doc.pop("_id", None)
            test_cases.append(tc_doc)

        # Deduplicate by id
        seen_ids = set()
        unique = []
        for tc in test_cases:
            tc_id = tc.get("id")
            if tc_id and tc_id not in seen_ids:
                seen_ids.add(tc_id)
                unique.append(tc)
            elif not tc_id:
                unique.append(tc)

        return unique

    @staticmethod
    def _detect_language(challenge: dict) -> str:
        """Detect the primary language from starter_code or default to python."""
        starter = challenge.get("starter_code", {})
        if isinstance(starter, dict):
            # Prefer python, then javascript, then whatever's available
            for lang in ["python", "javascript", "typescript", "go", "cpp", "java", "rust"]:
                if starter.get(lang):
                    return lang
        return "python"
