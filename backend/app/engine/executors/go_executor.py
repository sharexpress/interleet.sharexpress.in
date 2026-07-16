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

"""Go Executor — compiles with go build, runs native binary"""
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor


class GoExecutor(BaseExecutor):
    language = Language.GO
    docker_image = "interleet-go:latest"
    filename = "solution.go"
    compile_command = ["sh", "-c", "go build -o solution solution.go 2>&1"]
    run_command = ["sh", "-c", "./solution < stdin.txt"]
    requires_compile = True
