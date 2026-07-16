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

"""TypeScript Executor — compiles with tsc, runs with Node.js"""
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor


class TypeScriptExecutor(BaseExecutor):
    language = Language.TYPESCRIPT
    docker_image = "interleet-typescript:latest"
    filename = "solution.ts"
    compile_command = ["sh", "-c", "tsc --skipLibCheck --typeRoots /node_modules/@types --types node --target ES2020 --module commonjs solution.ts 2>&1"]
    run_command = ["sh", "-c", "node solution.js < stdin.txt"]
    requires_compile = True
