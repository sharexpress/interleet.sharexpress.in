"""
Partial Logic Mutant
Generates code that reads input but only handles the first/simplest case.
Simulates a submission that implements partial requirements.
"""

from __future__ import annotations

from typing import Any

from app.engine.validation.mutants.base import MutantStrategy


class PartialLogicMutant(MutantStrategy):
    @property
    def name(self) -> str:
        return "partial_logic"

    @property
    def description(self) -> str:
        return "Handles only the first/simplest case, ignores other branches"

    def generate(self, language: str, sample_test_cases: list[dict[str, Any]]) -> str:
        """
        Generates code that reads input and always returns the output of
        the first test case, regardless of what the actual input is.
        This simulates a partial implementation that only handles one branch.
        """
        if not sample_test_cases:
            return ""

        first_expected = sample_test_cases[0].get("expected_output", "").strip()

        if language == "python":
            return (
                "import sys\n"
                "data = sys.stdin.read()  # read but ignore\n"
                f"print({repr(first_expected)})\n"
            )
        elif language in ("javascript", "typescript"):
            escaped = first_expected.replace('"', '\\"')
            return (
                'const fs = require("fs");\n'
                'const data = fs.readFileSync("/dev/stdin", "utf8");  // read but ignore\n'
                f'console.log("{escaped}");\n'
            )
        elif language == "go":
            escaped = first_expected.replace('"', '\\"')
            return (
                'package main\n\nimport (\n\t"bufio"\n\t"fmt"\n\t"os"\n)\n\n'
                'func main() {\n'
                '\tscanner := bufio.NewScanner(os.Stdin)\n'
                '\tscanner.Scan() // read but ignore\n'
                f'\tfmt.Println("{escaped}")\n'
                '}\n'
            )
        elif language == "cpp":
            escaped = first_expected.replace('"', '\\"')
            return (
                '#include <iostream>\n#include <string>\n\n'
                'int main() {\n'
                '    std::string line;\n'
                '    std::getline(std::cin, line);  // read but ignore\n'
                f'    std::cout << "{escaped}" << std::endl;\n'
                '    return 0;\n'
                '}\n'
            )
        elif language == "java":
            escaped = first_expected.replace('"', '\\"')
            return (
                'import java.util.Scanner;\n\n'
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        Scanner sc = new Scanner(System.in);\n'
                '        if (sc.hasNextLine()) sc.nextLine();  // read but ignore\n'
                f'        System.out.println("{escaped}");\n'
                '    }\n'
                '}\n'
            )
        elif language == "rust":
            escaped = first_expected.replace('"', '\\"')
            return (
                'use std::io::Read;\n\n'
                'fn main() {\n'
                '    let mut input = String::new();\n'
                '    std::io::stdin().read_to_string(&mut input).unwrap();  // read but ignore\n'
                f'    println!("{escaped}");\n'
                '}\n'
            )

        return f"print({repr(first_expected)})\n"
