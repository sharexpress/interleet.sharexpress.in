import asyncio
from app.engine.executors.factory import ExecutorFactory
from app.engine.schemas import TestCaseSchema, ExecuteRequest
from app.engine.enums import Language

async def main():
    print("=== Testing Docker Compose Sandbox ===")
    
    executor = ExecutorFactory.get(Language.PYTHON, execution_mode="compose")
    
    # A simple docker-compose file that runs a python HTTP server
    docker_compose_yml = """
version: '3.8'
services:
  web:
    image: python:3.12-alpine
    command: sh -c "echo 'hello from compose' > index.html && python -m http.server 8080"
    ports:
      - "8080:8080"
"""

    # Verification script: wait for server, curl it, assert output
    verification_script = """#!/bin/bash
# Wait for the service to be up
for i in {1..10}; do
    curl -s http://localhost:8080 > output.txt
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 1
done

content=$(cat output.txt)
if [ "$content" = "hello from compose" ]; then
    echo -n "OK"
else
    echo -n "FAIL: $content"
fi
"""

    tc = TestCaseSchema(
        stdin="",
        expected_output="OK",
        verification_script=verification_script
    )

    req = ExecuteRequest(
        language=Language.PYTHON,
        code=docker_compose_yml,
        execution_mode="compose",
        comparison_mode="exact"
    )

    result = await executor.execute(req, tc)
    
    tc_result = result.testcase_results[0]
    print(f"Passed: {tc_result.passed}")
    print(f"Verdict: {tc_result.verdict}")
    print(f"Exit Code: {tc_result.exit_code}")
    print(f"Output: {tc_result.stdout}")
    print(f"Stderr: {tc_result.stderr}")

if __name__ == "__main__":
    asyncio.run(main())
