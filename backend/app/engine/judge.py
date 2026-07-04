"""
Interleet Judge Engine — Judge & Scoring Logic
Determines verdicts and scores for testcase results.

Comparison Pipeline (layered, short-circuits on first match):
  1. Exact Match         — raw string equality
  2. Trimmed Match       — strip per-line trailing whitespace
  3. Token Match         — whitespace-agnostic token comparison
  4. Semantic Structure  — parse as JSON/Python literals, deep-compare
  5. Numeric Tolerance   — floating-point epsilon comparison
  6. Line-by-Line Semantic — per-line structured comparison
  7. Normalized Fallback — lowercase, strip all formatting
"""

from __future__ import annotations

import ast
import json
import logging
import math
import re
from typing import Any, Optional

from app.engine.enums import ComparisonMode, Verdict
from app.engine.schemas import (
    SandboxResult,
    ScoringResult,
    TestCaseResult,
    TestCaseSchema,
)
from app.engine.comparators import get_custom_comparator

logger = logging.getLogger(__name__)

# Default tolerance for floating-point comparisons
FLOAT_EPSILON = 1e-6


class JudgeEngine:
    """
    Evaluates sandbox output against expected output and produces a Verdict.
    Supports exact, trimmed, token, semantic, and unordered comparison modes.
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

        # Per-testcase comparison_mode override takes priority
        effective_mode = testcase.comparison_mode or comparison_mode

        # Determine display stdout — show explicit message when empty
        display_stdout = sandbox_result.stdout
        if not testcase.hidden and not display_stdout.strip() and sandbox_result.exit_code != 0:
            display_stdout = "(no output produced)"
        elif not testcase.hidden and not display_stdout.strip() and sandbox_result.stderr.strip():
            display_stdout = "(no output produced — see stderr below)"

        # Build base result
        result = TestCaseResult(
            testcase_id=testcase.id,
            name=testcase.name,
            hidden=testcase.hidden,
            category=testcase.category.value if testcase.category else None,
            stdout="" if testcase.hidden else display_stdout,
            expected_output="" if testcase.hidden else testcase.expected_output,
            stderr=sandbox_result.stderr,  # Always preserve stderr (even for hidden)
            compile_output=compile_output,
            wall_time_ms=sandbox_result.wall_time_ms,
            runtime_ms=sandbox_result.wall_time_ms,  # Frontend-friendly alias
            peak_memory_mb=sandbox_result.peak_memory_mb,
            exit_code=sandbox_result.exit_code,
            weight=testcase.weight,
            screenshot_actual=sandbox_result.screenshot_base64,
            screenshot_expected=testcase.expected_output if effective_mode == ComparisonMode.VISUAL else None,
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

        # Compare output using the layered comparison pipeline
        output_matches, dom_diff = JudgeEngine._compare(
            sandbox_result=sandbox_result,
            expected=testcase.expected_output,
            mode=effective_mode,
            problem_slug=testcase.problem_slug,
        )
        
        result.dom_diff = dom_diff

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

    # ─── Category-aware scoring (anti-overfitting) ──────────────────────────

    @staticmethod
    def score_by_category(results: list[TestCaseResult]) -> dict:
        """
        Group results by test case category and return per-category pass rates.
        Used for anti-overfitting detection: a submission is only truly ACCEPTED
        if ALL categories pass, not just sample tests.

        Returns:
            {
                "all_categories_pass": bool,
                "category_scores": {
                    "sample": {"passed": 2, "total": 2},
                    "functional": {"passed": 5, "total": 5},
                    ...
                }
            }
        """
        from collections import defaultdict

        categories: dict[str, list[TestCaseResult]] = defaultdict(list)
        for r in results:
            cat = r.category or "functional"
            categories[cat].append(r)

        category_scores = {}
        all_pass = True
        for cat, cat_results in categories.items():
            passed = sum(1 for r in cat_results if r.passed)
            total = len(cat_results)
            category_scores[cat] = {"passed": passed, "total": total}
            if passed < total:
                all_pass = False

        return {
            "all_categories_pass": all_pass,
            "category_scores": category_scores,
        }

    # ─── Core Comparison Pipeline ──────────────────────────────────────────

    @staticmethod
    def _compare(sandbox_result: SandboxResult, expected: str, mode: ComparisonMode, problem_slug: Optional[str] = None) -> tuple[bool, Optional[dict]]:
        """
        Layered comparison pipeline. Each layer is progressively more lenient.
        Short-circuits on the first match. Returns (is_match, diff_data).
        """
        actual = sandbox_result.stdout

        # ── Custom Comparator Match ───────────────────────────────────
        if mode == ComparisonMode.CUSTOM and problem_slug:
            custom_comp = get_custom_comparator(problem_slug)
            if custom_comp:
                try:
                    return custom_comp(actual, expected), None
                except Exception as exc:
                    logger.warning("Custom comparator error for %s: %s", problem_slug, exc)
                    # fall back to standard semantic pipeline if custom fails

        # ── DOM Structural Match ──────────────────────────────────────
        if mode == ComparisonMode.DOM:
            if not sandbox_result.dom_content:
                return False, {"error": "No DOM content captured"}
            return _dom_match(sandbox_result.dom_content, expected)
            
        # ── Visual Pixel Match ────────────────────────────────────────
        if mode == ComparisonMode.VISUAL:
            if not sandbox_result.screenshot_base64:
                return False, {"error": "No screenshot captured"}
            return _visual_match(sandbox_result.screenshot_base64, expected)

        # ── JSON Structural Match ─────────────────────────────────────
        if mode == ComparisonMode.JSON:
            return _json_match(actual, expected), None

        # ── Layer 1: Exact Match ──────────────────────────────────────
        if actual == expected:
            return True, None

        if mode == ComparisonMode.EXACT:
            return False, None

        # ── Layer 2: Trimmed Match ────────────────────────────────────
        if _trimmed_match(actual, expected):
            return True, None

        if mode == ComparisonMode.TRIMMED:
            return _semantic_pipeline(actual, expected), None

        # ── Layer 3: Token Match ──────────────────────────────────────
        if _token_match(actual, expected):
            return True, None

        if mode == ComparisonMode.TOKEN:
            return _semantic_pipeline(actual, expected), None

        # ── SEMANTIC & UNORDERED: Full pipeline ───────────────────────
        if mode == ComparisonMode.UNORDERED:
            if _unordered_match(actual, expected):
                return True, None

        return _semantic_pipeline(actual, expected), None

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


# ═══════════════════════════════════════════════════════════════════════════════
# Comparison Helpers (module-level for testability)
# ═══════════════════════════════════════════════════════════════════════════════


def _json_match(actual: str, expected: str) -> bool:
    """Compare raw strings as parsed JSON objects or arrays."""
    try:
        act_val = json.loads(actual.strip())
        exp_val = json.loads(expected.strip())
        return _deep_equals(act_val, exp_val)
    except Exception:
        # Fallback: extract json from stdout if debug prints are included
        try:
            act_clean = actual.strip()
            match = re.search(r'(\{.*\}|\[.*\])', act_clean, re.DOTALL)
            if match:
                act_val = json.loads(match.group(1))
                exp_val = json.loads(expected.strip())
                return _deep_equals(act_val, exp_val)
        except Exception:
            pass
    return False


def _trimmed_match(actual: str, expected: str) -> bool:
    """Layer 2: Strip trailing whitespace per line, normalize newlines."""
    actual_lines = [
        line.rstrip()
        for line in actual.replace("\r\n", "\n").rstrip("\n").splitlines()
    ]
    expected_lines = [
        line.rstrip()
        for line in expected.replace("\r\n", "\n").rstrip("\n").splitlines()
    ]
    return actual_lines == expected_lines


def _token_match(actual: str, expected: str) -> bool:
    """Layer 3: Split on whitespace and compare tokens."""
    return actual.split() == expected.split()


def _unordered_match(actual: str, expected: str) -> bool:
    """Compare output lines as unordered sets (for problems where order doesn't matter)."""
    actual_lines = sorted(
        line.strip()
        for line in actual.replace("\r\n", "\n").strip().splitlines()
        if line.strip()
    )
    expected_lines = sorted(
        line.strip()
        for line in expected.replace("\r\n", "\n").strip().splitlines()
        if line.strip()
    )
    if actual_lines == expected_lines:
        return True

    # Also try semantic comparison on each sorted pair
    if len(actual_lines) == len(expected_lines):
        return all(
            _semantic_value_match(a, e)
            for a, e in zip(actual_lines, expected_lines)
        )
    return False


def _semantic_pipeline(actual: str, expected: str) -> bool:
    """
    Layers 4–7: The full semantic comparison pipeline.
    Tries structured parsing, numeric tolerance, line-by-line, and normalized fallback.
    """
    act_clean = actual.replace("\r\n", "\n").strip()
    exp_clean = expected.replace("\r\n", "\n").strip()

    # ── Layer 4: Semantic Structure Match ─────────────────────────
    if _semantic_value_match(act_clean, exp_clean):
        return True

    # ── Layer 5: Numeric Tolerance ────────────────────────────────
    if _numeric_match(act_clean, exp_clean):
        return True

    # ── Layer 6: Line-by-Line Semantic Match ──────────────────────
    if _line_by_line_semantic(act_clean, exp_clean):
        return True

    # ── Layer 7: Normalized Fallback ──────────────────────────────
    if _normalized_match(act_clean, exp_clean):
        return True

    return False


# ─── Layer 4: Semantic Value Match ─────────────────────────────────────────

def _parse_value(s: str) -> Any:
    """
    Parse a string into a Python value.
    Tries JSON first, then Python literal_eval, then boolean/null constants.
    Returns the original string if nothing parses.
    """
    s_stripped = s.strip()
    if not s_stripped:
        return s_stripped

    # Try JSON
    try:
        return json.loads(s_stripped)
    except (json.JSONDecodeError, ValueError):
        pass

    # Try Python literal_eval (handles True, False, None, tuples, etc.)
    try:
        return ast.literal_eval(s_stripped)
    except (ValueError, SyntaxError):
        pass

    # Handle standalone boolean/null constants across languages
    lower = s_stripped.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if lower in ("null", "none", "nil"):
        return None

    return s_stripped


def _deep_equals(a: Any, b: Any, epsilon: float = FLOAT_EPSILON) -> bool:
    """
    Recursively compare two parsed values with:
    - Dict comparison (order-insensitive keys)
    - List comparison (order-sensitive elements)
    - Float tolerance
    - Cross-language type normalization
    """
    # Normalize cross-language types
    a = _normalize_value(a)
    b = _normalize_value(b)

    # Both None
    if a is None and b is None:
        return True

    # Both booleans
    if isinstance(a, bool) and isinstance(b, bool):
        return a == b

    # Both numeric (int or float, but not bool)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if not isinstance(a, bool) and not isinstance(b, bool):
            if isinstance(a, float) or isinstance(b, float):
                return math.isclose(float(a), float(b), rel_tol=epsilon, abs_tol=epsilon)
            return a == b

    # Both strings
    if isinstance(a, str) and isinstance(b, str):
        return a == b

    # Both dicts — key-order-insensitive
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(_deep_equals(a[k], b[k], epsilon) for k in a)

    # Both lists/tuples — element-order-sensitive
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return False
        return all(_deep_equals(x, y, epsilon) for x, y in zip(a, b))

    # Fallback: string comparison of repr
    return str(a) == str(b)


def _normalize_value(v: Any) -> Any:
    """Normalize cross-language value representations."""
    if isinstance(v, str):
        lower = v.lower().strip()
        if lower == "true":
            return True
        if lower == "false":
            return False
        if lower in ("null", "none", "nil"):
            return None
        # Try to parse string-wrapped numbers
        try:
            if "." in v:
                return float(v)
            return int(v)
        except (ValueError, TypeError):
            pass
    return v


def _semantic_value_match(actual: str, expected: str) -> bool:
    """Parse both values and deep-compare with type normalization."""
    try:
        parsed_act = _parse_value(actual)
        parsed_exp = _parse_value(expected)

        # Only use semantic comparison if at least one side parsed to a non-string type
        act_is_structured = not isinstance(parsed_act, str)
        exp_is_structured = not isinstance(parsed_exp, str)

        if act_is_structured or exp_is_structured:
            return _deep_equals(parsed_act, parsed_exp)
    except Exception:
        pass
    return False


# ─── Layer 5: Numeric Tolerance ────────────────────────────────────────────

def _numeric_match(actual: str, expected: str) -> bool:
    """Compare as floating-point numbers with epsilon tolerance."""
    try:
        a = float(actual)
        e = float(expected)
        return math.isclose(a, e, rel_tol=FLOAT_EPSILON, abs_tol=FLOAT_EPSILON)
    except (ValueError, TypeError):
        pass
    return False


# ─── Layer 6: Line-by-Line Semantic Match ──────────────────────────────────

def _line_by_line_semantic(actual: str, expected: str) -> bool:
    """
    Split into lines and compare each line through the semantic pipeline.
    Handles multiline outputs where each line is a separate value/object.
    """
    actual_lines = [l.strip() for l in actual.splitlines() if l.strip()]
    expected_lines = [l.strip() for l in expected.splitlines() if l.strip()]

    if len(actual_lines) != len(expected_lines):
        return False

    if not actual_lines:
        return True

    for act_line, exp_line in zip(actual_lines, expected_lines):
        # Try direct string match first
        if act_line == exp_line:
            continue
        # Try semantic value match
        if _semantic_value_match(act_line, exp_line):
            continue
        # Try numeric match
        if _numeric_match(act_line, exp_line):
            continue
        # Try normalized match
        if _normalize_string(act_line) == _normalize_string(exp_line):
            continue
        return False

    return True


# ─── Layer 7: Normalized Fallback ──────────────────────────────────────────

_BRACKET_RE = re.compile(r'\s*([\[\],(){}:])\s*')
_WHITESPACE_RE = re.compile(r'\s+')


def _normalize_string(s: str) -> str:
    """Aggressively normalize a string for last-resort comparison."""
    val = s.lower().strip()
    val = val.replace("\r\n", "\n")
    val = _WHITESPACE_RE.sub(" ", val)
    val = _BRACKET_RE.sub(r'\1', val)
    val = val.strip("'\"")
    # Normalize boolean/null representations
    val = val.replace("true", "1").replace("false", "0")
    val = val.replace("none", "null")
    return val


def _normalized_match(actual: str, expected: str) -> bool:
    """Layer 7: Aggressively normalize and compare."""
    return _normalize_string(actual) == _normalize_string(expected)


# ─── Visual & DOM Matchers ──────────────────────────────────────────────────

def _dom_match(actual_html: str, expected_html: str) -> tuple[bool, Optional[dict]]:
    try:
        from bs4 import BeautifulSoup
        act_soup = BeautifulSoup(actual_html, "html.parser")
        exp_soup = BeautifulSoup(expected_html, "html.parser")
        
        # Strip all whitespace strings
        for text in act_soup.find_all(string=True):
            if text.strip() == "":
                text.extract()
        for text in exp_soup.find_all(string=True):
            if text.strip() == "":
                text.extract()

        def _canonicalize_element(el):
            if getattr(el, 'name', None) is None:
                return str(el).strip()
            # Sort classes
            if 'class' in el.attrs:
                el.attrs['class'].sort()
            # Sort all attributes
            attrs = sorted([(k, str(v)) for k, v in el.attrs.items()])
            children = [_canonicalize_element(c) for c in el.contents]
            return {"tag": el.name, "attrs": attrs, "children": children}
        
        # If we expect just the body or a specific fragment, we should compare only the body if present.
        act_node = act_soup.body if act_soup.body else act_soup
        exp_node = exp_soup.body if exp_soup.body else exp_soup

        act_canon = _canonicalize_element(act_node)
        exp_canon = _canonicalize_element(exp_node)
        
        # Compare canonicalized trees
        if act_canon == exp_canon:
            return True, None
        return False, {"actual_structure": act_canon, "expected_structure": exp_canon}
    except ImportError:
        logger.warning("BeautifulSoup not installed. Cannot perform DOM match.")
        return False, {"error": "DOM comparison not available."}
    except Exception as e:
        logger.error("DOM match error: %s", e)
        return False, {"error": str(e)}


def _visual_match(actual_b64: str, expected_b64: str) -> tuple[bool, Optional[dict]]:
    try:
        import base64
        import io
        from PIL import Image
        import pixelmatch

        # Remove data URI prefixes if present
        if actual_b64.startswith("data:image"):
            actual_b64 = actual_b64.split(",", 1)[1]
        if expected_b64.startswith("data:image"):
            expected_b64 = expected_b64.split(",", 1)[1]

        act_bytes = base64.b64decode(actual_b64)
        exp_bytes = base64.b64decode(expected_b64)

        act_img = Image.open(io.BytesIO(act_bytes)).convert("RGBA")
        exp_img = Image.open(io.BytesIO(exp_bytes)).convert("RGBA")

        # Must be same size for pixelmatch
        if act_img.size != exp_img.size:
            return False, {
                "error": "Size mismatch", 
                "actual_size": act_img.size, 
                "expected_size": exp_img.size
            }

        diff_img = Image.new("RGBA", act_img.size)
        mismatch_pixels = pixelmatch.pixelmatch(
            act_img, exp_img, diff_img,
            act_img.width, act_img.height,
            threshold=0.1, includeAA=True
        )

        total_pixels = act_img.width * act_img.height
        mismatch_percentage = mismatch_pixels / total_pixels

        # Allow 1% difference
        success = mismatch_percentage <= 0.01
        
        return success, {
            "mismatch_pixels": mismatch_pixels,
            "mismatch_percentage": round(mismatch_percentage * 100, 2),
            "threshold": 1.0,
            "passed": success
        }

    except ImportError:
        logger.warning("Pillow or pixelmatch not installed. Cannot perform VISUAL match.")
        return False, {"error": "Visual comparison not available."}
    except Exception as e:
        logger.error("Visual match error: %s", e)
        return False, {"error": str(e)}
