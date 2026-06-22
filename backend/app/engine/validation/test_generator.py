"""
Interleet Challenge Validation — Test Generator
Executes sandboxed Python generator code to produce randomized test cases.
Uses a reference solution to compute expected outputs.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from app.engine.enums import TestCaseCategory

logger = logging.getLogger(__name__)


class TestGenerator:
    """
    Generates randomized test cases for a challenge by:
    1. Running a Python generator function with a seed → produces stdin
    2. Running a reference solution against that stdin → produces expected_output
    3. Packaging the result as a test case with category=RANDOMIZED
    """

    async def generate(
        self,
        generator_code: str,
        seed: int,
        reference_code: str,
        reference_language: str,
        problem_slug: str,
    ) -> Optional[dict[str, Any]]:
        """
        Generate a single randomized test case.

        Args:
            generator_code: Python code defining generate_test_case(seed) → str.
            seed: Random seed for reproducibility.
            reference_code: The canonical reference solution.
            reference_language: Language of the reference solution.
            problem_slug: Problem this test case belongs to.

        Returns:
            Test case dict or None on failure.
        """
        try:
            # Step 1: Generate stdin by running the generator
            stdin = await self._run_generator(generator_code, seed)
            if stdin is None:
                logger.warning("Generator returned None for seed=%d", seed)
                return None

            # Step 2: Run reference solution to get expected output
            expected_output = await self._run_reference(
                reference_code, reference_language, stdin,
            )
            if expected_output is None:
                logger.warning("Reference solution failed for seed=%d", seed)
                return None

            # Step 3: Package as test case
            return {
                "id": f"gen-{problem_slug}-{seed}-{str(uuid4())[:8]}",
                "problem_slug": problem_slug,
                "name": f"Randomized test (seed={seed})",
                "stdin": stdin,
                "expected_output": expected_output,
                "hidden": True,
                "weight": 1.0,
                "category": TestCaseCategory.RANDOMIZED.value,
                "created_at": datetime.utcnow().isoformat(),
                "created_by": "test_generator",
            }

        except Exception as exc:
            logger.exception("Test generation failed for seed=%d: %s", seed, exc)
            return None

    async def generate_batch(
        self,
        generator_code: str,
        count: int,
        reference_code: str,
        reference_language: str,
        problem_slug: str,
        start_seed: int = 1,
    ) -> list[dict[str, Any]]:
        """
        Generate a batch of randomized test cases with sequential seeds.

        Args:
            generator_code: Python generator code.
            count: Number of test cases to generate.
            reference_code: Canonical reference solution.
            reference_language: Language of the reference.
            problem_slug: Problem slug.
            start_seed: Starting seed value.

        Returns:
            List of generated test case dicts.
        """
        results = []
        for seed in range(start_seed, start_seed + count):
            tc = await self.generate(
                generator_code=generator_code,
                seed=seed,
                reference_code=reference_code,
                reference_language=reference_language,
                problem_slug=problem_slug,
            )
            if tc is not None:
                results.append(tc)

        logger.info(
            "Generated %d/%d randomized test cases for '%s'",
            len(results), count, problem_slug,
        )
        return results

    async def _run_generator(self, generator_code: str, seed: int) -> Optional[str]:
        """
        Execute the generator code in a sandbox to produce stdin.
        The generator must define: generate_test_case(seed) -> str
        """
        try:
            from app.engine.executors.factory import ExecutorFactory
            from app.engine.schemas import TestCaseSchema

            # Wrap the generator code to call generate_test_case(seed)
            wrapped_code = (
                f"{generator_code}\n\n"
                f"if __name__ == '__main__':\n"
                f"    result = generate_test_case({seed})\n"
                f"    print(result, end='')\n"
            )

            executor = ExecutorFactory.get("python")
            tc = TestCaseSchema(id="gen", stdin="", expected_output="")
            sandbox_result, compile_result = await executor.run_testcase(
                code=wrapped_code,
                testcase=tc,
                time_limit=10.0,
                memory_limit=256,
            )

            if sandbox_result.exit_code != 0:
                logger.warning(
                    "Generator failed: exit=%d stderr=%s",
                    sandbox_result.exit_code, sandbox_result.stderr[:500],
                )
                return None

            return sandbox_result.stdout

        except Exception as exc:
            logger.exception("Generator execution failed: %s", exc)
            return None

    async def _run_reference(
        self, code: str, language: str, stdin: str,
    ) -> Optional[str]:
        """
        Execute the reference solution in a sandbox with the given stdin.
        """
        try:
            from app.engine.executors.factory import ExecutorFactory
            from app.engine.schemas import TestCaseSchema

            executor = ExecutorFactory.get(language)
            tc = TestCaseSchema(id="ref", stdin=stdin, expected_output="")
            sandbox_result, compile_result = await executor.run_testcase(
                code=code,
                testcase=tc,
                time_limit=10.0,
                memory_limit=256,
            )

            if sandbox_result.exit_code != 0:
                logger.warning(
                    "Reference solution failed: exit=%d stderr=%s",
                    sandbox_result.exit_code, sandbox_result.stderr[:500],
                )
                return None

            return sandbox_result.stdout

        except Exception as exc:
            logger.exception("Reference execution failed: %s", exc)
            return None
