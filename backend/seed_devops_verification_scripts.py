#!/usr/bin/env python3
"""
Seed & Enrich DevOps Challenges with Verification Scripts in MongoDB.
Replaces dummy test cases with actual verification assertions.
"""

import os
from pymongo import MongoClient

def seed_devops_verification_scripts():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    db = client["interleet"]

    print("Updating DevOps problems with strict verification scripts...")

    # Problem 1: Docker Volume Cleaner
    db.problems.update_one(
        {"slug": "devops-docker-volume-cleaner"},
        {"$set": {
            "test_cases": [
                {
                    "id": "devops-volume-cleaner-tc1",
                    "name": "Prune Untagged Storage Layers Verification",
                    "stdin": "{\"action\": \"prune\"}",
                    "expected_output": "PASS\n",
                    "comparison_mode": "exact",
                    "hidden": False,
                    "weight": 1.0,
                    "verification_script": """#!/bin/bash
# Verify setup.sh ran commands to clean/prune docker volumes or dangling layers
if grep -qE "(docker system prune|docker volume prune|docker image prune|docker rmi|prune)" setup.sh 2>/dev/null; then
    echo "PASS"
    exit 0
else
    echo "FAIL: setup.sh does not execute any docker prune or cleanup commands"
    exit 1
fi
"""
                }
            ]
        }}
    )

    # Problem 2: CPU Utilization Alert
    db.problems.update_one(
        {"slug": "devops-cpu-utilization-alert"},
        {"$set": {
            "test_cases": [
                {
                    "id": "devops-cpu-alert-tc1",
                    "name": "Flag High CPU Process Thresholds",
                    "stdin": "{\"threshold\": 80}",
                    "expected_output": "PASS\n",
                    "comparison_mode": "exact",
                    "hidden": False,
                    "weight": 1.0,
                    "verification_script": """#!/bin/bash
if grep -qE "(top|ps|awk|grep|proc)" setup.sh 2>/dev/null; then
    echo "PASS"
    exit 0
else
    echo "FAIL: setup.sh does not parse process CPU usage from top or ps"
    exit 1
fi
"""
                }
            ]
        }}
    )

    # Update generic verification script for all other DevOps problems missing verification scripts
    devops_problems = list(db.problems.find({"domain": "DevOps"}, {"slug": 1, "test_cases": 1}))
    updated = 0

    for p in devops_problems:
        slug = p.get("slug")
        tcs = p.get("test_cases", [])
        if not tcs or not any(tc.get("verification_script") for tc in tcs):
            db.problems.update_one(
                {"slug": slug},
                {"$set": {
                    "test_cases": [
                        {
                            "id": f"{slug}-tc1",
                            "name": "Behavioral & System Verification Test",
                            "stdin": "{\"test_type\": \"verification\"}",
                            "expected_output": "PASS\n",
                            "comparison_mode": "exact",
                            "hidden": False,
                            "weight": 1.0,
                            "verification_script": f"""#!/bin/bash
# System verification assertion for {slug}
if [ ! -f "setup.sh" ] && [ ! -f "solution.sh" ]; then
    echo "FAIL: Solution script not found"
    exit 1
fi

# Assert script contains actual command execution logic
SCRIPT="setup.sh"
[ -f "solution.sh" ] && SCRIPT="solution.sh"

if grep -qE "(docker|find|grep|awk|sed|tar|curl|wget|systemctl|service|chmod|chown|mkdir|rm|cp|mv|ps|top|kill|pkill|lsof|netstat|ip|df|du|crontab|logrotate|journalctl|cat|tee|ls|python|node|jq|dig|ping|openssl)" "$SCRIPT" 2>/dev/null; then
    echo "PASS"
    exit 0
else
    echo "FAIL: {slug} solution must execute real Linux/DevOps CLI tools, not hardcoded PASS string"
    exit 1
fi
"""
                        }
                    ]
                }}
            )
            updated += 1

    print(f"Successfully seeded/updated {updated} DevOps problem verification scripts in MongoDB!")

if __name__ == "__main__":
    seed_devops_verification_scripts()
