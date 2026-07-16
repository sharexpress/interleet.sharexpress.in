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
    HTML = "html"
    MULTI = "multi"


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
    JSON = "json"              # Direct JSON structural validation
    CUSTOM = "custom"          # Specialized validation logic for complex challenges
    DOM = "dom"                # Semantic HTML DOM diffing
    VISUAL = "visual"          # Pixel-by-pixel screenshot comparison


class TestCaseCategory(str, Enum):
    SAMPLE = "sample"           # Visible examples shown to candidates
    FUNCTIONAL = "functional"   # Hidden normal/functional tests
    EDGE_CASE = "edge_case"     # Hidden edge-case tests
    ADVERSARIAL = "adversarial" # Hidden adversarial tests (anti-cheat)
    RANDOMIZED = "randomized"   # Hidden randomized tests (anti-memorization)
