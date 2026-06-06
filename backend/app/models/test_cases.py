"""
Test Cases Model — Interleet Judge Engine
Represents a single test case for a coding challenge.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


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

    # Configuration
    hidden: bool = False  # If True, output is redacted from API responses
    weight: float = 1.0   # Relative weight for scoring (default = equal weight)
    name: Optional[str] = None  # Display name, e.g., "Edge case: empty list"

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
