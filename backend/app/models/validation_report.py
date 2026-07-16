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
Validation Report Model — Interleet Challenge Validation Framework
Persists the result of running the quality gate on a challenge.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class ValidationReport(BaseModel):
    """
    Stored in MongoDB `validation_reports` collection.
    Created each time the quality gate is run on a challenge.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    challenge_slug: str

    # Coverage scores
    coverage_score: float = 0.0         # % of category requirements met (0–100)
    mutation_resistance: float = 0.0    # % of mutants rejected (0–100)
    edge_case_coverage: str = "FAIL"    # "PASS" or "FAIL"

    # Detailed breakdown
    test_counts: Dict[str, int] = {}              # {category: count}
    minimum_requirements: Dict[str, int] = {}     # {category: minimum_required}
    category_deficiencies: Dict[str, int] = {}    # {category: shortfall}
    mutant_results: List[Dict[str, Any]] = []     # Per-mutant pass/fail

    # Gate result
    passed: bool = False
    blocking_reasons: List[str] = []

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
