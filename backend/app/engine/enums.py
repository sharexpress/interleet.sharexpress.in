"""
Interleet Judge Engine — Enumerations
All enum types used throughout the execution engine.
"""

from enum import Enum


class Language(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    CPP = "cpp"
    RUST = "rust"
    JAVA = "java"


class Verdict(str, Enum):
    ACCEPTED = "ACCEPTED"
    WRONG_ANSWER = "WRONG_ANSWER"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    MEMORY_LIMIT_EXCEEDED = "MEMORY_LIMIT_EXCEEDED"
    COMPILATION_ERROR = "COMPILATION_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ExecutionStatus(str, Enum):
    QUEUED = "QUEUED"
    COMPILING = "COMPILING"
    RUNNING = "RUNNING"
    JUDGING = "JUDGING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class WebSocketEventType(str, Enum):
    QUEUED = "queued"
    COMPILING = "compiling"
    RUNNING = "running"
    JUDGING = "judging"
    COMPLETED = "completed"
    FAILED = "failed"
    HEARTBEAT = "heartbeat"


class ComparisonMode(str, Enum):
    EXACT = "exact"
    TRIMMED = "trimmed"
    TOKEN = "token"
    SEMANTIC = "semantic"      # Smart structured comparison (JSON/Python literals)
    UNORDERED = "unordered"    # Order-independent comparison (sets, dicts)


class TestCaseCategory(str, Enum):
    SAMPLE = "sample"           # Visible examples shown to candidates
    FUNCTIONAL = "functional"   # Hidden normal/functional tests
    EDGE_CASE = "edge_case"     # Hidden edge-case tests
    ADVERSARIAL = "adversarial" # Hidden adversarial tests (anti-cheat)
    RANDOMIZED = "randomized"   # Hidden randomized tests (anti-memorization)
