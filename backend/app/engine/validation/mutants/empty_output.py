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
Empty Output Mutant
Generates code that produces no output at all.
If this passes, the challenge likely has missing or empty expected outputs.
"""

from __future__ import annotations

from typing import Any

from app.engine.validation.mutants.base import MutantStrategy


class EmptyOutputMutant(MutantStrategy):
    @property
    def name(self) -> str:
        return "empty_output"

    @property
    def description(self) -> str:
        return "Produces no output at all (empty program)"

    def generate(self, language: str, sample_test_cases: list[dict[str, Any]]) -> str:
        if language == "python":
            return "pass\n"
        elif language in ("javascript", "typescript"):
            return "// empty\n"
        elif language == "go":
            return "package main\n\nfunc main() {}\n"
        elif language == "cpp":
            return "int main() { return 0; }\n"
        elif language == "java":
            return (
                "public class Main {\n"
                "    public static void main(String[] args) {}\n"
                "}\n"
            )
        elif language == "rust":
            return "fn main() {}\n"

        return "pass\n"
