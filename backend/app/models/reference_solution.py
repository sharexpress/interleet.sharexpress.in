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
Reference Solution Model — Interleet Challenge Validation Framework
Stores canonical reference implementations for challenges.
Kept in a separate collection from challenges for security isolation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class ReferenceSolution(BaseModel):
    """
    Stored in MongoDB `reference_solutions` collection.
    Reference solutions are never exposed through public challenge APIs.
    Used by the validation engine to:
      - Generate expected output for randomized tests
      - Serve as the baseline for differential testing
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    challenge_slug: str

    language: str               # python, javascript, typescript, go, cpp, rust, java
    code: str

    is_primary: bool = True     # The canonical solution used for test generation
    description: Optional[str] = None  # Optional notes about the solution approach

    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
