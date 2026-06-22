"""
Sample-Only Mutant
Generates code that checks if the input matches a sample test case input,
and outputs the corresponding expected output. Falls back to a default otherwise.
This simulates a submission that only handles the visible examples.
"""

from __future__ import annotations

from typing import Any

from app.engine.validation.mutants.base import MutantStrategy


class SampleOnlyMutant(MutantStrategy):
    @property
    def name(self) -> str:
        return "sample_only"

    @property
    def description(self) -> str:
        return "Matches sample inputs exactly and outputs sample expected outputs"

    def generate(self, language: str, sample_test_cases: list[dict[str, Any]]) -> str:
        if not sample_test_cases:
            return ""

        if language == "python":
            return self._generate_python(sample_test_cases)
        elif language in ("javascript", "typescript"):
            return self._generate_js(sample_test_cases)
        elif language == "go":
            return self._generate_go(sample_test_cases)
        elif language == "cpp":
            return self._generate_cpp(sample_test_cases)
        elif language == "java":
            return self._generate_java(sample_test_cases)
        elif language == "rust":
            return self._generate_rust(sample_test_cases)

        return self._generate_python(sample_test_cases)

    def _generate_python(self, test_cases: list[dict[str, Any]]) -> str:
        lines = ["import sys\n", "stdin = sys.stdin.read()\n"]
        for i, tc in enumerate(test_cases):
            stdin = repr(tc.get("stdin", "").strip())
            expected = repr(tc.get("expected_output", "").strip())
            keyword = "if" if i == 0 else "elif"
            lines.append(f'{keyword} stdin.strip() == {stdin}:\n')
            lines.append(f'    print({expected})\n')
        lines.append('else:\n    print("unknown")\n')
        return "".join(lines)

    def _generate_js(self, test_cases: list[dict[str, Any]]) -> str:
        lines = [
            'const fs = require("fs");\n',
            'const stdin = fs.readFileSync("/dev/stdin", "utf8").trim();\n',
        ]
        for i, tc in enumerate(test_cases):
            stdin = tc.get("stdin", "").strip().replace('"', '\\"')
            expected = tc.get("expected_output", "").strip().replace('"', '\\"')
            keyword = "if" if i == 0 else "} else if"
            lines.append(f'{keyword} (stdin === "{stdin}") {{\n')
            lines.append(f'  console.log("{expected}");\n')
        lines.append('} else {\n  console.log("unknown");\n}\n')
        return "".join(lines)

    def _generate_go(self, test_cases: list[dict[str, Any]]) -> str:
        lines = [
            'package main\n\nimport (\n\t"bufio"\n\t"fmt"\n\t"os"\n\t"strings"\n)\n\n',
            'func main() {\n',
            '\tscanner := bufio.NewScanner(os.Stdin)\n',
            '\tvar sb strings.Builder\n',
            '\tfor scanner.Scan() {\n\t\tsb.WriteString(scanner.Text())\n\t\tsb.WriteString("\\n")\n\t}\n',
            '\tstdin := strings.TrimSpace(sb.String())\n',
        ]
        for i, tc in enumerate(test_cases):
            stdin = tc.get("stdin", "").strip().replace('"', '\\"')
            expected = tc.get("expected_output", "").strip().replace('"', '\\"')
            keyword = "\tif" if i == 0 else " else if"
            lines.append(f'{keyword} stdin == "{stdin}" {{\n')
            lines.append(f'\t\tfmt.Println("{expected}")\n')
            lines.append("\t}")
        lines.append(' else {\n\t\tfmt.Println("unknown")\n\t}\n}\n')
        return "".join(lines)

    def _generate_cpp(self, test_cases: list[dict[str, Any]]) -> str:
        lines = [
            '#include <iostream>\n#include <string>\n#include <sstream>\n\n',
            'int main() {\n',
            '    std::ostringstream oss;\n',
            '    oss << std::cin.rdbuf();\n',
            '    std::string input = oss.str();\n',
            '    // trim\n',
            '    while (!input.empty() && (input.back() == \'\\n\' || input.back() == \' \')) input.pop_back();\n',
        ]
        for i, tc in enumerate(test_cases):
            stdin = tc.get("stdin", "").strip().replace('"', '\\"')
            expected = tc.get("expected_output", "").strip().replace('"', '\\"')
            keyword = "    if" if i == 0 else " else if"
            lines.append(f'{keyword} (input == "{stdin}") {{\n')
            lines.append(f'        std::cout << "{expected}" << std::endl;\n')
            lines.append("    }")
        lines.append(' else {\n        std::cout << "unknown" << std::endl;\n    }\n')
        lines.append("    return 0;\n}\n")
        return "".join(lines)

    def _generate_java(self, test_cases: list[dict[str, Any]]) -> str:
        lines = [
            'import java.util.Scanner;\n\n',
            'public class Main {\n',
            '    public static void main(String[] args) {\n',
            '        Scanner sc = new Scanner(System.in);\n',
            '        StringBuilder sb = new StringBuilder();\n',
            '        while (sc.hasNextLine()) sb.append(sc.nextLine()).append("\\n");\n',
            '        String input = sb.toString().trim();\n',
        ]
        for i, tc in enumerate(test_cases):
            stdin = tc.get("stdin", "").strip().replace('"', '\\"')
            expected = tc.get("expected_output", "").strip().replace('"', '\\"')
            keyword = "        if" if i == 0 else " else if"
            lines.append(f'{keyword} (input.equals("{stdin}")) {{\n')
            lines.append(f'            System.out.println("{expected}");\n')
            lines.append("        }")
        lines.append(' else {\n            System.out.println("unknown");\n        }\n')
        lines.append("    }\n}\n")
        return "".join(lines)

    def _generate_rust(self, test_cases: list[dict[str, Any]]) -> str:
        lines = [
            'use std::io::Read;\n\n',
            'fn main() {\n',
            '    let mut input = String::new();\n',
            '    std::io::stdin().read_to_string(&mut input).unwrap();\n',
            '    let input = input.trim();\n',
        ]
        for i, tc in enumerate(test_cases):
            stdin = tc.get("stdin", "").strip().replace('"', '\\"')
            expected = tc.get("expected_output", "").strip().replace('"', '\\"')
            keyword = "    if" if i == 0 else " else if"
            lines.append(f'{keyword} input == "{stdin}" {{\n')
            lines.append(f'        println!("{expected}");\n')
            lines.append("    }")
        lines.append(' else {\n        println!("unknown");\n    }\n}\n')
        return "".join(lines)
