from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import uuid4
from enum import Enum


class SubmissionStatus(str, Enum):
    pending = "pending"
    running = "running"
    accepted = "accepted"
    wrong_answer = "wrong_answer"
    runtime_error = "runtime_error"
    compilation_error = "compilation_error"
    time_limit_exceeded = "time_limit_exceeded"
    memory_limit_exceeded = "memory_limit_exceeded"
    failed = "failed"


class SubmissionType(str, Enum):
    challenge = "challenge"
    interview = "interview"
    system_design = "system_design"


class ProgrammingLanguage(str, Enum):
    javascript = "javascript"
    typescript = "typescript"
    python = "python"
    java = "java"
    cpp = "cpp"
    go = "go"
    rust = "rust"


class TestCaseResult(BaseModel):
    test_case_id: str

    passed: bool = False

    execution_time_ms: int = 0

    memory_used_mb: int = 0

    expected_output: Optional[str] = None

    actual_output: Optional[str] = None

    error_message: Optional[str] = None


class SubmissionScore(BaseModel):
    score: int = 0

    frontend_score: int = 0

    backend_score: int = 0

    fullstack_score: int = 0

    devops_score: int = 0


class SubmissionModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    user_id: str

    challenge_id: Optional[str] = None

    interview_id: Optional[str] = None

    submission_type: SubmissionType

    language: ProgrammingLanguage

    code: str

    status: SubmissionStatus = SubmissionStatus.pending

    passed_test_cases: int = 0

    total_test_cases: int = 0

    execution_time_ms: int = 0

    memory_used_mb: int = 0

    test_case_results: List[TestCaseResult] = []

    score: SubmissionScore = SubmissionScore()

    feedback: Optional[str] = None

    ai_review: Optional[str] = None

    plagiarism_score: int = 0

    xp_earned: int = 0

    submitted_at: datetime = Field(default_factory=datetime.utcnow)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ─────────────────────────────────────────────────────────────────────
# Engine Submission Model (Docker-based judge engine)
# ─────────────────────────────────────────────────────────────────────

class EngineSubmissionModel(BaseModel):
    """
    Submission record created by the Docker-based judge engine.
    Stored in the `engine_submissions` MongoDB collection.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    job_id: str = ""

    # Identity
    user_id: Optional[str] = None
    problem_slug: Optional[str] = None
    challenge_id: Optional[str] = None

    # Submission content
    language: str
    code: str = ""
    mode: str = "run"  # "run" | "submit"

    # Results
    status: str = "QUEUED"
    verdict: Optional[str] = None
    score: float = 0.0
    passed_testcases: int = 0
    total_testcases: int = 0

    # Performance metrics
    time_seconds: float = 0.0
    memory_mb: float = 0.0

    # Raw outputs
    stdout: str = ""
    stderr: str = ""
    compile_output: str = ""
    exit_code: int = 0

    # Per-testcase breakdown
    testcase_results: List[Dict[str, Any]] = []

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
