"""
Interleet Judge Engine — Code Security Guard
Scans submitted code for dangerous patterns before running in Docker.
This is a pre-flight static check (not a replacement for sandboxing).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class GuardResult:
    allowed: bool
    reason: Optional[str] = None


# ─── Per-language blocked patterns ────────────────────────────────────────────

_PYTHON_BLOCKED = [
    # OS / process / network access
    (r"\bimport\s+os\b",                  "Use of 'os' module is not allowed"),
    (r"\bimport\s+sys\b",                 "Use of 'sys' module is not allowed"),
    (r"\bimport\s+subprocess\b",          "Use of 'subprocess' module is not allowed"),
    (r"\bimport\s+socket\b",              "Use of 'socket' module is not allowed"),
    (r"\bimport\s+requests?\b",           "Use of 'requests' module is not allowed"),
    (r"\bimport\s+urllib\b",              "Use of 'urllib' module is not allowed"),
    (r"\bimport\s+http\b",                "Use of 'http' module is not allowed"),
    (r"\bimport\s+shutil\b",              "Use of 'shutil' module is not allowed"),
    (r"\bimport\s+pathlib\b",             "Use of 'pathlib' module is not allowed"),
    (r"\bimport\s+tempfile\b",            "Use of 'tempfile' module is not allowed"),
    (r"\bimport\s+threading\b",           "Use of 'threading' module is not allowed"),
    (r"\bimport\s+multiprocessing\b",     "Use of 'multiprocessing' module is not allowed"),
    (r"\bimport\s+ctypes\b",              "Use of 'ctypes' module is not allowed"),
    (r"\bimport\s+importlib\b",           "Use of 'importlib' module is not allowed"),
    # Dynamic execution
    (r"\b__import__\s*\(",                "Dynamic imports are not allowed"),
    (r"\beval\s*\(",                      "eval() is not allowed"),
    (r"\bexec\s*\(",                      "exec() is not allowed"),
    (r"\bcompile\s*\(",                   "compile() is not allowed"),
    # File I/O
    (r"\bopen\s*\(",                      "File I/O is not allowed"),
    # Shell / memory
    (r"/etc/passwd",                      "Access to system files is not allowed"),
    (r"/proc/",                           "Access to /proc is not allowed"),
    (r"\bos\s*\.\s*system\b",             "os.system() is not allowed"),
    (r"\bos\s*\.\s*popen\b",              "os.popen() is not allowed"),
    (r"\bos\s*\.\s*execv?\b",             "os.exec*() is not allowed"),
    (r"\bos\s*\.\s*fork\b",               "os.fork() is not allowed"),
    # Infinite memory heuristic — 10^8+ in a single literal is suspicious
    (r"\b10\s*\*\*\s*[89]\d*\b",         "Potential memory exhaustion: very large literal"),
]

_JAVASCRIPT_BLOCKED = [
    # Block dangerous require() modules specifically — NOT all require() calls.
    # require('fs') is allowed for reading stdin in the Docker sandbox.
    (r"""require\s*\(\s*['"]child_process['"]\s*\)""",  "child_process module is not allowed"),
    (r"""require\s*\(\s*['"]cluster['"]\s*\)""",        "cluster module is not allowed"),
    (r"""require\s*\(\s*['"]net['"]\s*\)""",            "net module is not allowed"),
    (r"""require\s*\(\s*['"]http['"]\s*\)""",           "http module is not allowed"),
    (r"""require\s*\(\s*['"]https['"]\s*\)""",          "https module is not allowed"),
    (r"""require\s*\(\s*['"]dgram['"]\s*\)""",          "dgram module is not allowed"),
    (r"""require\s*\(\s*['"]tls['"]\s*\)""",            "tls module is not allowed"),
    (r"""require\s*\(\s*['"]os['"]\s*\)""",             "os module is not allowed"),
    (r"""require\s*\(\s*['"]v8['"]\s*\)""",             "v8 module is not allowed"),
    (r"""require\s*\(\s*['"]vm['"]\s*\)""",             "vm module is not allowed"),
    (r"""require\s*\(\s*['"]worker_threads['"]\s*\)""", "worker_threads module is not allowed"),
    (r"""require\s*\(\s*['"]repl['"]\s*\)""",           "repl module is not allowed"),
    # process restrictions
    (r"\bprocess\s*\.\s*env\b",           "process.env access is not allowed"),
    (r"\bprocess\s*\.\s*exit\b",          "process.exit() is not allowed"),
    (r"\bprocess\s*\.\s*binding\b",       "process.binding() is not allowed"),
    # Shell execution
    (r"\bexecSync\b",                     "execSync is not allowed"),
    (r"\bspawnSync\b",                    "spawnSync is not allowed"),
    (r"\bspawn\s*\(",                     "spawn() is not allowed"),
    # Dangerous FS writes (reads are OK for stdin)
    (r"\bfs\s*\.\s*(write|unlink|rm|mkdir|chmod|chown)\b", "Destructive file system operations are not allowed"),
    # Network
    (r"\bnet\s*\.\s*create",              "Network access is not allowed"),
    (r"\bhttp\s*\.\s*request\b",          "HTTP requests are not allowed"),
    (r"\bfetch\s*\(",                     "fetch() is not allowed in sandbox"),
    # Dynamic code execution
    (r"\beval\s*\(",                      "eval() is not allowed"),
    (r"\bnew\s+Function\s*\(",            "new Function() is not allowed"),
]

_TYPESCRIPT_BLOCKED = _JAVASCRIPT_BLOCKED  # same rules

_GO_BLOCKED = [
    (r'"os/exec"',                        "'os/exec' import is not allowed"),
    (r'"net/http"',                       "'net/http' import is not allowed"),
    (r'"syscall"',                        "'syscall' import is not allowed"),
    (r'"unsafe"',                         "'unsafe' import is not allowed"),
    (r'"os"\b',                           "'os' import is not allowed"),
    (r'"io/ioutil"',                      "'io/ioutil' import is not allowed"),
    (r'"net"',                            "'net' import is not allowed"),
]

_JAVA_BLOCKED = [
    (r"Runtime\.getRuntime\(\)",          "Runtime.exec() is not allowed"),
    (r"ProcessBuilder",                   "ProcessBuilder is not allowed"),
    (r"import\s+java\.io\.",              "java.io imports are not allowed"),
    (r"import\s+java\.net\.",             "java.net imports are not allowed"),
    (r"import\s+java\.lang\.reflect\.",   "Reflection is not allowed"),
    (r"System\.exit\s*\(",                "System.exit() is not allowed"),
]

_CPP_BLOCKED = [
    (r'#include\s*[<"]sys/',              "sys/ headers are not allowed"),
    (r'#include\s*[<"]unistd\.h[>"]',    "unistd.h is not allowed"),
    (r'\bsystem\s*\(',                    "system() is not allowed"),
    (r'\bpopen\s*\(',                     "popen() is not allowed"),
    (r'\bfork\s*\(',                      "fork() is not allowed"),
    (r'\bexecv\w*\s*\(',                  "exec*() is not allowed"),
]

_RUST_BLOCKED = [
    (r'use\s+std\s*::\s*process',        "std::process is not allowed"),
    (r'use\s+std\s*::\s*net',            "std::net is not allowed"),
    (r'use\s+std\s*::\s*fs',             "std::fs is not allowed"),
    (r'\bCommand\s*::new\b',             "Command::new() is not allowed"),
]

_LANG_RULES: dict[str, list[tuple[str, str]]] = {
    "python":     _PYTHON_BLOCKED,
    "javascript": _JAVASCRIPT_BLOCKED,
    "typescript": _TYPESCRIPT_BLOCKED,
    "go":         _GO_BLOCKED,
    "java":       _JAVA_BLOCKED,
    "cpp":        _CPP_BLOCKED,
    "rust":       _RUST_BLOCKED,
}

# Universal rules applied to every language
_UNIVERSAL_BLOCKED = [
    (r"/etc/passwd",                      "Access to system files is not allowed"),
    (r"/proc/self",                       "Access to /proc/self is not allowed"),
    (r"127\.0\.0\.1|localhost",           "Localhost network access is not allowed"),
]


# ─── Main Guard ───────────────────────────────────────────────────────────────

class CodeGuard:
    """
    Static code analysis guard.
    Call CodeGuard.check(code, language) before submitting to Docker.
    """

    @classmethod
    def check(cls, code: str, language: str) -> GuardResult:
        """
        Scan `code` for dangerous patterns based on `language`.
        Returns GuardResult(allowed=True) if clean, else GuardResult(allowed=False, reason=...).
        """
        lang_rules = _LANG_RULES.get(language.lower(), [])
        all_rules = lang_rules + _UNIVERSAL_BLOCKED

        for pattern, reason in all_rules:
            if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
                return GuardResult(allowed=False, reason=reason)

        # Heuristic: code length cap (1 MB)
        if len(code) > 1_000_000:
            return GuardResult(allowed=False, reason="Code size exceeds the 1 MB limit")

        return GuardResult(allowed=True)
