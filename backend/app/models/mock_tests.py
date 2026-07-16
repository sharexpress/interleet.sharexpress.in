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

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class RoleEnum(str, Enum):
    frontend = "frontend"
    backend = "backend"
    devops = "devops"
    hr = "hr"
    behavioural = "behavioural"


class InterviewTypeEnum(str, Enum):
    technical = "technical"
    behavioural = "behavioural"
    hr = "hr"


class DifficultyEnum(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class MockTestModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    role: RoleEnum
    interview_type: InterviewTypeEnum
    difficulty: DifficultyEnum
    jd: str
    additional_context: Optional[str] = None
    total_questions: int = 8
    easy_questions: int = 2
    medium_questions: int = 3
    hard_questions: int = 3
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
