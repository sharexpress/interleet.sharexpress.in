"""
Constant Output Mutant
Generates code that always prints a constant value (1, 0, true, false, empty).
If this passes, the challenge has insufficient output diversity.
"""

from __future__ import annotations

from typing import Any

from app.engine.validation.mutants.base import MutantStrategy


class ConstantOutputMutant(MutantStrategy):
    @property
    def name(self) -> str:
        return "constant_output"

    @property
    def description(self) -> str:
        return "Always prints a constant value regardless of input"

    def generate(self, language: str, sample_test_cases: list[dict[str, Any]]) -> str:
        # Guess a likely constant from sample outputs
        constants = set()
        for tc in sample_test_cases:
            out = tc.get("expected_output", "").strip().lower()
            if out in ("true", "false", "0", "1", "yes", "no"):
                constants.add(out)

        # Pick the most common output, or "1" as default
        constant = next(iter(constants), "1")

        if language == "python":
            return f'print("{constant}")\n'
        elif language in ("javascript", "typescript"):
            return f'console.log("{constant}");\n'
        elif language == "go":
            return (
                'package main\n\nimport "fmt"\n\n'
                f'func main() {{\n\tfmt.Println("{constant}")\n}}\n'
            )
        elif language == "cpp":
            return (
                '#include <iostream>\n'
                f'int main() {{ std::cout << "{constant}" << std::endl; return 0; }}\n'
            )
        elif language == "java":
            return (
                'public class Main {\n'
                f'    public static void main(String[] args) {{ System.out.println("{constant}"); }}\n'
                '}\n'
            )
        elif language == "rust":
            return f'fn main() {{ println!("{constant}"); }}\n'

        return f'print("{constant}")\n'
