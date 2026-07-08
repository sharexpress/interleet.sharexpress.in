"""
Interleet Judge Engine — Pydantic v2 Schemas
Request/response models for all engine APIs.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator

from app.engine.enums import (
    ComparisonMode,
    ExecutionStatus,
    Language,
    TestCaseCategory,
    Verdict,
    WebSocketEventType,
)


# ─────────────────────────────────────────────
# Request Schemas
# ─────────────────────────────────────────────

class ExecuteRequest(BaseModel):
    """POST /api/v1/execute — one-shot fire and wait"""

    language: Language
    code: str
    stdin: str = ""
    expected_output: Optional[str] = None
    time_limit: float = Field(default=5.0, ge=0.5, le=30.0, description="Seconds")
    memory_limit: int = Field(default=256, ge=32, le=1024, description="MB")
    comparison_mode: ComparisonMode = ComparisonMode.TRIMMED
    execution_mode: str = "cli"  # "cli", "http", "browser", "devops"
    runtime: Optional[str] = None


class InlineTestCase(BaseModel):
    """Lightweight test case passed inline from the frontend."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    stdin: str = ""
    expected_output: str = ""
    name: Optional[str] = None
    hidden: bool = False


class RunRequest(BaseModel):
    """POST /api/v1/run — run against sample test cases provided inline by the frontend."""
    language: Language
    code: str
    test_cases: list[InlineTestCase] = []
    time_limit: float = Field(default=5.0, ge=0.5, le=30.0, description="Seconds")
    memory_limit: int = Field(default=256, ge=32, le=1024, description="MB")
    comparison_mode: ComparisonMode = ComparisonMode.TRIMMED
    execution_mode: str = "cli"  # "cli", "http", "browser", "devops"
    runtime: Optional[str] = None


class SubmissionRequest(ExecuteRequest):
    """POST /api/v1/submissions — async submission linked to a problem"""

    user_id: Optional[str] = None
    problem_slug: Optional[str] = None
    challenge_id: Optional[str] = None
    contest_id: Optional[str] = None
    mode: str = "submit"  # "run" | "submit"



# ─────────────────────────────────────────────
# Sandbox / Execution Primitives
# ─────────────────────────────────────────────

class SandboxResult(BaseModel):
    """Raw output from a Docker container run"""

    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    wall_time_ms: float = 0.0
    peak_memory_mb: float = 0.0
    timed_out: bool = False
    oom_killed: bool = False
    
    # Visual / DOM Sandbox properties (populated by Browser Runtime)
    screenshot_base64: Optional[str] = None
    dom_content: Optional[str] = None


class CompileResult(BaseModel):
    """Result of a compilation step"""

    success: bool
    output: str = ""
    error: str = ""
    time_ms: float = 0.0


# ─────────────────────────────────────────────
# Test Case Schema
# ─────────────────────────────────────────────

class TestCaseSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    problem_slug: str = ""
    stdin: str = ""
    expected_output: str = ""
    verification_script: Optional[str] = None
    files: Optional[dict[str, str]] = None
    hidden: bool = False
    weight: float = 1.0
    category: Optional[TestCaseCategory] = None  # Test case classification
    time_limit: Optional[float] = None   # per-testcase override
    memory_limit: Optional[int] = None   # per-testcase override
    name: Optional[str] = None
    comparison_mode: Optional[ComparisonMode] = None  # per-testcase comparison override


class TestCaseResult(BaseModel):
    """Per-testcase execution result"""

    testcase_id: str
    name: Optional[str] = None
    hidden: bool = False
    passed: bool = False
    verdict: Verdict = Verdict.INTERNAL_ERROR
    category: Optional[str] = None  # Test case category for per-category scoring
    # Hidden testcases redact actual vs expected
    stdout: str = ""
    expected_output: str = ""
    stderr: str = ""
    compile_output: str = ""
    wall_time_ms: float = 0.0
    runtime_ms: float = 0.0  # Frontend-friendly alias for wall_time_ms
    peak_memory_mb: float = 0.0
    exit_code: int = 0
    weight: float = 1.0
    revealed_input: Optional[str] = None
    revealed_expected: Optional[str] = None
    
    # Visual / DOM diff properties
    screenshot_actual: Optional[str] = None
    screenshot_expected: Optional[str] = None
    dom_diff: Optional[dict] = None



# ─────────────────────────────────────────────
# Full Execution Result
# ─────────────────────────────────────────────

class StepEvent(BaseModel):
    id: str
    title: str
    status: str  # "passed", "failed", "pending"
    startedAt: int = 0
    endedAt: int = 0
    durationMs: int = 0
    stdout: str = ""
    stderr: str = ""

class ExecutionResult(BaseModel):
    """Final result returned to caller"""

    runtime: Optional[dict] = None  # Injected from registry
    steps: list[StepEvent] = Field(default_factory=list)

    success: bool
    submission_id: str = Field(default_factory=lambda: str(uuid4()))
    status: ExecutionStatus = ExecutionStatus.COMPLETED
    verdict: Verdict = Verdict.INTERNAL_ERROR

    # Aggregate metrics
    stdout: str = ""
    stderr: str = ""
    compile_output: str = ""
    memory: float = 0.0      # MB
    time: float = 0.0        # seconds
    exit_code: int = 0

    # Per testcase breakdown (for submissions)
    testcase_results: list[TestCaseResult] = Field(default_factory=list)
    passed_testcases: int = 0
    total_testcases: int = 0
    score: float = 0.0

    # Per-category scoring breakdown (anti-overfitting)
    category_scores: Optional[CategoryScoringResult] = None

    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


# ─────────────────────────────────────────────
# Queue Job Schema
# ─────────────────────────────────────────────

class ExecutionJob(BaseModel):
    """Serialized job pushed to Redis queue"""

    job_id: str = Field(default_factory=lambda: str(uuid4()))
    submission_id: str
    language: Language
    code: str
    stdin: str = ""
    expected_output: Optional[str] = None
    time_limit: float = 5.0
    memory_limit: int = 256
    comparison_mode: ComparisonMode = ComparisonMode.TRIMMED
    execution_mode: str = "cli"
    runtime: Optional[str] = None
    problem_slug: Optional[str] = None
    challenge_id: Optional[str] = None
    user_id: Optional[str] = None
    contest_id: Optional[str] = None
    mode: str = "run"
    testcases: list[TestCaseSchema] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


    def to_redis(self) -> str:
        return self.model_dump_json()

    @classmethod
    def from_redis(cls, raw: str) -> "ExecutionJob":
        return cls.model_validate_json(raw)


# ─────────────────────────────────────────────
# WebSocket Event Schema
# ─────────────────────────────────────────────

class WebSocketEvent(BaseModel):
    """Streamed over WebSocket to frontend"""

    type: WebSocketEventType
    submission_id: str
    status: ExecutionStatus
    data: Optional[dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    def to_json(self) -> str:
        return self.model_dump_json()


# ─────────────────────────────────────────────
# Scoring Result
# ─────────────────────────────────────────────

class ScoringResult(BaseModel):
    verdict: Verdict
    score: float
    passed: int
    total: int
    max_time_ms: float = 0.0
    max_memory_mb: float = 0.0


class CategoryScoringResult(BaseModel):
    """Per-category scoring breakdown for anti-overfitting detection."""
    all_categories_pass: bool = False
    category_scores: dict[str, dict] = Field(default_factory=dict)
