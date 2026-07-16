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
Test Cases Model — Interleet Judge Engine
Represents a single test case for a coding challenge.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.engine.enums import TestCaseCategory


class TestCaseModel(BaseModel):
    """
    Stored in MongoDB `test_cases` collection.
    Linked to a problem via `problem_slug`.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    problem_slug: str

    # Input / Output
    stdin: str = ""
    expected_output: str = ""

    # Classification
    category: TestCaseCategory = TestCaseCategory.SAMPLE
    hidden: bool = False  # If True, output is redacted from API responses
    weight: float = 1.0   # Relative weight for scoring (default = equal weight)
    name: Optional[str] = None  # Display name, e.g., "Edge case: empty list"

    # Comparison
    comparison_mode: Optional[str] = None  # Per-testcase comparison override

    # Per-testcase limits (overrides problem-level limits if set)
    time_limit: Optional[float] = None     # seconds
    memory_limit: Optional[int] = None     # MB

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None  # admin user_id


class TestCaseBatch(BaseModel):
    """Batch create/update request for test cases."""
    problem_slug: str
    test_cases: list[TestCaseModel]
