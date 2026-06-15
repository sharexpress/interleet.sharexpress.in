"""
Interleet Judge Engine — Judge & Scoring Logic
Determines verdicts and scores for testcase results.
"""

from __future__ import annotations

import logging

from app.engine.enums import ComparisonMode, Verdict
from app.engine.schemas import (
    SandboxResult,
    ScoringResult,
    TestCaseResult,
    TestCaseSchema,
)

logger = logging.getLogger(__name__)


class JudgeEngine:
    """
    Evaluates sandbox output against expected output and produces a Verdict.
    Supports exact match, trimmed match, and token-based comparison.
    """

    # ─── Single testcase evaluation ────────────────────────────────────────

    @staticmethod
    def evaluate(
        sandbox_result: SandboxResult,
        testcase: TestCaseSchema,
        compile_output: str = "",
        comparison_mode: ComparisonMode = ComparisonMode.TRIMMED,
    ) -> TestCaseResult:
        """Produce a TestCaseResult for a single testcase run."""

        # Build base result
        result = TestCaseResult(
            testcase_id=testcase.id,
            name=testcase.name,
            hidden=testcase.hidden,
            stdout="" if testcase.hidden else sandbox_result.stdout,
            expected_output="" if testcase.hidden else testcase.expected_output,
            stderr=sandbox_result.stderr,
            compile_output=compile_output,
            wall_time_ms=sandbox_result.wall_time_ms,
            peak_memory_mb=sandbox_result.peak_memory_mb,
            exit_code=sandbox_result.exit_code,
            weight=testcase.weight,
        )

        # Check Memory Limit Exceeded
        if sandbox_result.oom_killed:
            result.verdict = Verdict.MEMORY_LIMIT_EXCEEDED
            result.passed = False
            return result

        # Check Time Limit Exceeded
        if sandbox_result.timed_out:
            result.verdict = Verdict.TIME_LIMIT_EXCEEDED
            result.passed = False
            return result

        # Check Compilation Error (non-zero exit + compile_output present)
        if compile_output and sandbox_result.exit_code != 0:
            result.verdict = Verdict.COMPILATION_ERROR
            result.passed = False
            return result

        # Check Runtime Error
        if sandbox_result.exit_code != 0:
            result.verdict = Verdict.RUNTIME_ERROR
            result.passed = False
            return result

        # Compare output
        output_matches = JudgeEngine._compare(
            actual=sandbox_result.stdout,
            expected=testcase.expected_output,
            mode=comparison_mode,
        )

        if output_matches:
            result.verdict = Verdict.ACCEPTED
            result.passed = True
        else:
            result.verdict = Verdict.WRONG_ANSWER
            result.passed = False

        return result

    # ─── Multi-testcase scoring ─────────────────────────────────────────────

    @staticmethod
    def score(results: list[TestCaseResult]) -> ScoringResult:
        """Aggregate multiple testcase results into an overall verdict + score."""

        if not results:
            return ScoringResult(
                verdict=Verdict.INTERNAL_ERROR,
                score=0.0,
                passed=0,
                total=0,
            )

        total_weight = sum(r.weight for r in results) or 1.0
        passed_weight = sum(r.weight for r in results if r.passed)
        score = round((passed_weight / total_weight) * 100, 2)
        passed = sum(1 for r in results if r.passed)
        total = len(results)

        max_time = max((r.wall_time_ms for r in results), default=0.0)
        max_mem = max((r.peak_memory_mb for r in results), default=0.0)

        # Determine aggregate verdict (worst-case priority)
        verdict = JudgeEngine._aggregate_verdict(results, passed, total)

        return ScoringResult(
            verdict=verdict,
            score=score,
            passed=passed,
            total=total,
            max_time_ms=max_time,
            max_memory_mb=max_mem,
        )

    # ─── Internal helpers ──────────────────────────────────────────────────

    @staticmethod
    def _compare(actual: str, expected: str, mode: ComparisonMode) -> bool:
        """Compare actual vs expected output with the given comparison mode."""
        # Clean basic trailing/leading spaces/newlines/carriage returns
        act_clean = actual.replace("\r\n", "\n").strip()
        exp_clean = expected.replace("\r\n", "\n").strip()

        matched = False
        if mode == ComparisonMode.EXACT:
            matched = actual == expected
        elif mode == ComparisonMode.TRIMMED:
            # Strip trailing whitespace per line, then compare
            actual_lines = [line.rstrip() for line in actual.replace("\r\n", "\n").rstrip("\n").splitlines()]
            expected_lines = [line.rstrip() for line in expected.replace("\r\n", "\n").rstrip("\n").splitlines()]
            matched = actual_lines == expected_lines
        elif mode == ComparisonMode.TOKEN:
            actual_tokens = actual.split()
            expected_tokens = expected.split()
            matched = actual_tokens == expected_tokens
        else:
            matched = act_clean == exp_clean

        if matched:
            return True

        # --- Forgiving Fallback comparison if strict fails ---
        import re
        def clean_and_normalize(s: str) -> str:
            # Lowercase
            val = s.lower().strip()
            # Replace carriage returns
            val = val.replace("\r\n", "\n")
            # Replace any run of whitespace/newlines with a single space
            val = re.sub(r'\s+', ' ', val)
            # Remove spaces around brackets, braces, parentheses, commas, colons
            val = re.sub(r'\s*([\[\],(){}:])\s*', r'\1', val)
            # Strip surrounding quotes
            val = val.strip("'\"")
            return val

        if clean_and_normalize(actual) == clean_and_normalize(expected):
            return True

        # Fallback check for boolean mappings (e.g. true vs 1, false vs 0)
        act_norm = clean_and_normalize(actual).replace("true", "1").replace("false", "0")
        exp_norm = clean_and_normalize(expected).replace("true", "1").replace("false", "0")
        if act_norm == exp_norm:
            return True

        return False

    @staticmethod
    def _aggregate_verdict(
        results: list[TestCaseResult],
        passed: int,
        total: int,
    ) -> Verdict:
        """Priority order: CE > MLE > TLE > RE > WA > AC"""

        verdicts = {r.verdict for r in results}

        if Verdict.COMPILATION_ERROR in verdicts:
            return Verdict.COMPILATION_ERROR
        if Verdict.INTERNAL_ERROR in verdicts:
            return Verdict.INTERNAL_ERROR
        if Verdict.MEMORY_LIMIT_EXCEEDED in verdicts:
            return Verdict.MEMORY_LIMIT_EXCEEDED
        if Verdict.TIME_LIMIT_EXCEEDED in verdicts:
            return Verdict.TIME_LIMIT_EXCEEDED
        if Verdict.RUNTIME_ERROR in verdicts:
            return Verdict.RUNTIME_ERROR
        if passed < total:
            return Verdict.WRONG_ANSWER
        return Verdict.ACCEPTED
