"""
Hardcoded Output Mutant
Generates code that prints the expected output of the FIRST sample test case.
If this passes all tests, the challenge is trivially exploitable.
"""

from __future__ import annotations

from typing import Any

from app.engine.validation.mutants.base import MutantStrategy


class HardcodedOutputMutant(MutantStrategy):
    @property
    def name(self) -> str:
        return "hardcoded_output"

    @property
    def description(self) -> str:
        return "Prints the expected output of the first sample test case verbatim"

    def generate(self, language: str, sample_test_cases: list[dict[str, Any]]) -> str:
        if not sample_test_cases:
            return ""

        expected = sample_test_cases[0].get("expected_output", "").strip()

        if language == "python":
            return f'print({repr(expected)})\n'
        elif language in ("javascript", "typescript"):
            escaped = expected.replace("\\", "\\\\").replace("`", "\\`")
            return f'console.log(`{escaped}`);\n'
        elif language == "go":
            escaped = expected.replace('"', '\\"')
            return (
                'package main\n\nimport "fmt"\n\n'
                f'func main() {{\n\tfmt.Println("{escaped}")\n}}\n'
            )
        elif language == "cpp":
            escaped = expected.replace('"', '\\"')
            return (
                '#include <iostream>\n'
                f'int main() {{ std::cout << "{escaped}" << std::endl; return 0; }}\n'
            )
        elif language == "java":
            escaped = expected.replace('"', '\\"')
            return (
                'public class Main {\n'
                f'    public static void main(String[] args) {{ System.out.println("{escaped}"); }}\n'
                '}\n'
            )
        elif language == "rust":
            escaped = expected.replace('"', '\\"')
            return f'fn main() {{ println!("{escaped}"); }}\n'

        return f'print({repr(expected)})\n'  # fallback to Python
