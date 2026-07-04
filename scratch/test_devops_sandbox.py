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
        expected_output="OK\\n",
        verification_script=verification_script
    )

    results = await executor.run_batch_testcases(
        code=code,
        testcases=[tc],
        time_limit=5.0,
        memory_limit=256
    )

    result = results[0]
    print(f"Passed: {result.passed}")
    print(f"Verdict: {result.verdict}")
    print(f"Exit Code: {result.exit_code}")
    print(f"Output (Verification Script): {result.stdout}")

if __name__ == "__main__":
    asyncio.run(main())
