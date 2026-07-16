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

import asyncio
from app.engine.executors.factory import ExecutorFactory
from app.engine.schemas import TestCaseSchema
from app.engine.enums import Language

async def main():
    print("=== Testing DevOps Sandbox ===")
    
    executor = ExecutorFactory.get(Language.PYTHON, execution_mode="devops")
    
    # User tries to create a file at /tmp/test.txt with content "hello"
    code = """#!/bin/bash
echo "hello" > /tmp/test.txt
"""

    # Verification script asserts the file exists and has "hello"
    verification_script = """#!/bin/bash
if [ -f /tmp/test.txt ]; then
    content=$(cat /tmp/test.txt)
    if [ "$content" = "hello" ]; then
        echo "OK"
    else
        echo "FAIL_CONTENT"
    fi
else
    echo "FAIL_NOT_FOUND"
fi
"""

    tc = TestCaseSchema(
        stdin="",
        expected_output="OK\n",
        verification_script=verification_script
    )

    from app.engine.schemas import ExecuteRequest
    
    req = ExecuteRequest(
        language=Language.PYTHON,
        code=code,
        execution_mode="devops",
        comparison_mode="exact"
    )

    result = await executor.execute(req, tc)
    
    tc_result = result.testcase_results[0]
    print(f"Passed: {tc_result.passed}")
    print(f"Verdict: {tc_result.verdict}")
    print(f"Exit Code: {tc_result.exit_code}")
    print(f"Output (Verification Script): {tc_result.stdout}")

if __name__ == "__main__":
    asyncio.run(main())
