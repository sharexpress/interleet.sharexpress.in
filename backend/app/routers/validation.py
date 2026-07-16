# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Interleet — Validation Router
Admin-only endpoints for challenge validation operations.
"""

from fastapi import APIRouter, Body, Depends, Query

from app.controllers.validation import ValidationController
from app.middleware.admin import AdminMiddleware

router = APIRouter(prefix="/challenges", tags=["Challenge Validation"])


@router.post(
    "/{slug}/validate",
    dependencies=[Depends(AdminMiddleware.is_admin)],
    summary="Run quality gate check",
    description=(
        "Run the full quality gate on a challenge without publishing it. "
        "Returns a detailed validation report with coverage score, "
        "mutation resistance, and blocking reasons."
    ),
)
async def validate_challenge(slug: str):
    return await ValidationController.run_quality_check(slug)


@router.get(
    "/{slug}/validation-report",
    dependencies=[Depends(AdminMiddleware.is_admin)],
    summary="Get latest validation report",
)
async def get_validation_report(slug: str):
    return await ValidationController.get_validation_report(slug)


@router.post(
    "/{slug}/reference-solution",
    dependencies=[Depends(AdminMiddleware.is_admin)],
    summary="Save reference solution",
    description=(
        "Save a canonical reference implementation for a challenge. "
        "Used for generating expected outputs and differential testing."
    ),
)
async def save_reference_solution(slug: str, payload: dict = Body(...)):
    return await ValidationController.save_reference_solution(slug, payload)


@router.get(
    "/{slug}/reference-solution",
    dependencies=[Depends(AdminMiddleware.is_admin)],
    summary="Get reference solution",
)
async def get_reference_solution(slug: str):
    return await ValidationController.get_reference_solution(slug)


@router.post(
    "/{slug}/test-generator",
    dependencies=[Depends(AdminMiddleware.is_admin)],
    summary="Save test generator code",
    description=(
        "Save Python generator code that defines generate_test_case(seed) -> str. "
        "Used for producing randomized test cases."
    ),
)
async def save_test_generator(slug: str, payload: dict = Body(...)):
    return await ValidationController.save_test_generator(slug, payload)


@router.post(
    "/{slug}/generate-tests",
    dependencies=[Depends(AdminMiddleware.is_admin)],
    summary="Generate randomized test cases",
    description=(
        "Run the test generator to produce randomized test cases. "
        "Requires a saved test generator and reference solution."
    ),
)
async def generate_tests(
    slug: str,
    count: int = Query(default=10, ge=1, le=100, description="Number of tests to generate"),
):
    return await ValidationController.generate_randomized_tests(slug, count)


@router.post(
    "/{slug}/differential-test",
    dependencies=[Depends(AdminMiddleware.is_admin)],
    summary="Run differential testing",
    description=(
        "Compare a candidate solution against the reference solution "
        "on randomly generated inputs."
    ),
)
async def differential_test(slug: str, payload: dict = Body(...)):
    return await ValidationController.run_differential_test(slug, payload)
