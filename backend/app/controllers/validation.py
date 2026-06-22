"""
Interleet — Validation Controller
Business logic for challenge validation operations:
  - Running the quality gate
  - Managing reference solutions
  - Managing test generators
  - Generating randomized test cases
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from fastapi import HTTPException

from app.core.db import get_db
from app.engine.validation.quality_gate import QualityGate
from app.engine.validation.test_generator import TestGenerator
from app.engine.validation.differential_tester import DifferentialTester

db = get_db()


class ValidationController:
    """Controller for all challenge validation operations."""

    # ─── Quality Gate ──────────────────────────────────────────────────────

    @staticmethod
    async def run_quality_check(
        slug: str,
        admin_user_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Run the quality gate on a challenge and return the report.
        Does NOT publish the challenge — just returns the validation result.
        """
        gate = QualityGate()
        report = await gate.evaluate(slug, admin_user_id=admin_user_id)

        # Persist the report
        report_dict = report.dict() if hasattr(report, "dict") else report.model_dump()
        await db.validation_reports.insert_one({**report_dict, "_created": True})

        # Update challenge with latest report
        await db.problems.update_one(
            {"slug": slug},
            {
                "$set": {
                    "is_validated": report.passed,
                    "validation_report": report_dict,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        return {
            "success": True,
            "passed": report.passed,
            "report": report_dict,
        }

    @staticmethod
    async def get_validation_report(slug: str) -> dict[str, Any]:
        """Get the latest validation report for a challenge."""
        report = await db.validation_reports.find_one(
            {"challenge_slug": slug},
            sort=[("created_at", -1)],
        )
        if not report:
            # Check embedded report in challenge
            challenge = await db.problems.find_one({"slug": slug})
            if challenge and challenge.get("validation_report"):
                return {
                    "success": True,
                    "report": challenge["validation_report"],
                }
            raise HTTPException(
                status_code=404,
                detail=f"No validation report found for '{slug}'",
            )

        report.pop("_id", None)
        return {"success": True, "report": report}

    # ─── Reference Solutions ───────────────────────────────────────────────

    @staticmethod
    async def save_reference_solution(slug: str, payload: dict) -> dict[str, Any]:
        """Save or update a reference solution for a challenge."""
        # Verify challenge exists
        challenge = await db.problems.find_one({"slug": slug})
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

        language = payload.get("language", "python")
        code = payload.get("code", "")
        is_primary = payload.get("is_primary", True)
        description = payload.get("description", "")

        if not code.strip():
            raise HTTPException(
                status_code=422,
                detail="Reference solution code cannot be empty",
            )

        solution_id = str(uuid4())

        # If this is primary, demote existing primary solutions
        if is_primary:
            await db.reference_solutions.update_many(
                {"challenge_slug": slug, "is_primary": True},
                {"$set": {"is_primary": False, "updated_at": datetime.utcnow()}},
            )

        solution_doc = {
            "id": solution_id,
            "challenge_slug": slug,
            "language": language,
            "code": code,
            "is_primary": is_primary,
            "description": description,
            "created_by": payload.get("created_by"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        await db.reference_solutions.insert_one(solution_doc)

        # Update challenge pointer
        if is_primary:
            await db.problems.update_one(
                {"slug": slug},
                {
                    "$set": {
                        "reference_solution_id": solution_id,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

        solution_doc.pop("_id", None)
        return {
            "success": True,
            "message": "Reference solution saved",
            "data": solution_doc,
        }

    @staticmethod
    async def get_reference_solution(slug: str) -> dict[str, Any]:
        """Get the primary reference solution for a challenge."""
        solution = await db.reference_solutions.find_one(
            {"challenge_slug": slug, "is_primary": True},
            sort=[("created_at", -1)],
        )
        if not solution:
            raise HTTPException(
                status_code=404,
                detail=f"No reference solution found for '{slug}'",
            )

        solution.pop("_id", None)
        return {"success": True, "data": solution}

    # ─── Test Generator ────────────────────────────────────────────────────

    @staticmethod
    async def save_test_generator(slug: str, payload: dict) -> dict[str, Any]:
        """Save test generator code for a challenge."""
        challenge = await db.problems.find_one({"slug": slug})
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

        generator_code = payload.get("generator_code", "")
        if not generator_code.strip():
            raise HTTPException(
                status_code=422,
                detail="Generator code cannot be empty",
            )

        await db.problems.update_one(
            {"slug": slug},
            {
                "$set": {
                    "test_generator_code": generator_code,
                    "test_generator_language": payload.get("language", "python"),
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        return {
            "success": True,
            "message": "Test generator saved",
        }

    @staticmethod
    async def generate_randomized_tests(
        slug: str,
        count: int = 10,
    ) -> dict[str, Any]:
        """
        Generate randomized test cases using the challenge's generator and
        reference solution. Persists generated tests to the database.
        """
        challenge = await db.problems.find_one({"slug": slug})
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

        generator_code = challenge.get("test_generator_code")
        if not generator_code:
            raise HTTPException(
                status_code=400,
                detail="Challenge has no test generator code. "
                       "Save one first via POST /challenges/{slug}/test-generator",
            )

        # Get reference solution
        ref_solution = await db.reference_solutions.find_one(
            {"challenge_slug": slug, "is_primary": True},
        )
        if not ref_solution:
            raise HTTPException(
                status_code=400,
                detail="Challenge has no reference solution. "
                       "Save one first via POST /challenges/{slug}/reference-solution",
            )

        # Generate test cases
        generator = TestGenerator()
        generated = await generator.generate_batch(
            generator_code=generator_code,
            count=count,
            reference_code=ref_solution["code"],
            reference_language=ref_solution["language"],
            problem_slug=slug,
        )

        if not generated:
            raise HTTPException(
                status_code=500,
                detail="Test generation failed — no test cases were produced. "
                       "Check generator code and reference solution.",
            )

        # Persist to test_cases collection
        for tc in generated:
            await db.test_cases.insert_one(tc)

        # Also append to embedded array in challenge
        existing_cases = challenge.get("test_cases", [])
        embedded_additions = [
            {
                "id": tc["id"],
                "name": tc["name"],
                "stdin": tc["stdin"],
                "expected_output": tc["expected_output"],
                "hidden": True,
                "weight": 1,
                "category": "randomized",
            }
            for tc in generated
        ]
        await db.problems.update_one(
            {"slug": slug},
            {
                "$set": {
                    "test_cases": existing_cases + embedded_additions,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        return {
            "success": True,
            "message": f"Generated {len(generated)} randomized test cases",
            "count": len(generated),
            "test_case_ids": [tc["id"] for tc in generated],
        }

    # ─── Differential Testing ──────────────────────────────────────────────

    @staticmethod
    async def run_differential_test(
        slug: str,
        payload: dict,
    ) -> dict[str, Any]:
        """
        Run differential testing between a candidate solution and the
        reference solution.
        """
        challenge = await db.problems.find_one({"slug": slug})
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

        generator_code = challenge.get("test_generator_code")
        if not generator_code:
            raise HTTPException(
                status_code=400,
                detail="Challenge has no test generator for differential testing",
            )

        ref_solution = await db.reference_solutions.find_one(
            {"challenge_slug": slug, "is_primary": True},
        )
        if not ref_solution:
            raise HTTPException(
                status_code=400,
                detail="Challenge has no reference solution",
            )

        candidate_code = payload.get("code", "")
        candidate_language = payload.get("language", "python")
        sample_count = payload.get("sample_count", 20)

        tester = DifferentialTester()
        report = await tester.compare(
            candidate_code=candidate_code,
            candidate_language=candidate_language,
            reference_code=ref_solution["code"],
            reference_language=ref_solution["language"],
            generator_code=generator_code,
            sample_count=sample_count,
        )

        return {
            "success": True,
            "report": report.to_dict(),
        }
