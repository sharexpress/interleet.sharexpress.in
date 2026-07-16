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

from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class ExecutionResultModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    execution_job_id: str
    submission_id: str | None = None
    problem_slug: str
    testcase_id: str
    judge0_token: str
    status: str
    verdict: str
    passed: bool = False
    runtime_ms: float | None = None
    memory_kb: int | None = None
    stdout: str = ""
    stderr: str = ""
    compile_output: str = ""
    analytics: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
