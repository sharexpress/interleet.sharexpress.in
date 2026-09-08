#!/usr/bin/env python3
# Copyright 2026 Sharexpress Contributors
"""
Automated Test Suite for SQL Practice Curriculum (53 Challenges)
Validates schema consistency, metadata, starter codes, and executes all
canonical solutions against the in-memory database runner.
"""

import sys
import os
import json
import time

# Add root backend and sandboxes runner to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(backend_dir)
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(workspace_dir, "sandboxes", "database"))

from runner import execute_sql
from sql_curriculum import ALL_SQL_CHALLENGES

def run_tests():
    print(f"================================================================================")
    print(f"  INTERLEET SQL CURRICULUM AUTOMATED TEST SUITE")
    print(f"  Testing {len(ALL_SQL_CHALLENGES)} SQL Challenges across 5 Case Studies")
    print(f"================================================================================\n")

    slugs = set()
    titles = set()
    total_test_cases = 0
    passed_test_cases = 0
    start_time = time.time()

    for idx, c in enumerate(ALL_SQL_CHALLENGES, 1):
        slug = c.get("slug")
        title = c.get("title")

        # 1. Uniqueness Checks
        assert slug, f"Challenge #{idx} missing slug"
        assert slug not in slugs, f"Duplicate slug: {slug}"
        slugs.add(slug)

        assert title, f"Challenge #{idx} missing title"
        assert title not in titles, f"Duplicate title: {title}"
        titles.add(title)

        # 2. Metadata Schema Validation
        assert c.get("domain") == "Databases", f"{slug}: domain must be Databases"
        assert c.get("runtime") == "database", f"{slug}: runtime must be database"
        assert c.get("execution_mode") == "database", f"{slug}: execution_mode must be database"
        assert set(c.get("technologies", [])) >= {"sql", "sqlite", "mysql", "postgresql"}, f"{slug}: missing required technologies"

        # 3. Starter Code Check
        starters = c.get("starter_code", {})
        for lang in ["sql", "sqlite", "mysql", "postgresql"]:
            assert lang in starters and len(starters[lang].strip()) > 0, f"{slug}: missing starter code for {lang}"

        # 4. Canonical Solution Check
        canonical = c.get("canonical_solution", "").strip()
        assert len(canonical) > 0, f"{slug}: missing canonical_solution"

        # 5. Execute Test Cases
        tcs = c.get("test_cases", [])
        assert len(tcs) >= 1, f"{slug}: challenge must have at least 1 test case"

        print(f"[{idx:02d}/53] Testing: {slug.ljust(38)} | {title[:28].ljust(28)}", end="", flush=True)

        for tc_idx, tc in enumerate(tcs, 1):
            total_test_cases += 1
            stdin_data = json.loads(tc["stdin"])
            schema_sql = stdin_data.get("schema_sql")
            fixtures = stdin_data.get("fixtures")
            expected = json.loads(tc["expected_output"])

            # Execute canonical solution in sandbox
            actual = execute_sql(canonical, schema_sql=schema_sql, fixtures=fixtures)

            assert actual == expected, (
                f"\nFAIL: {slug} (TC #{tc_idx})\n"
                f"Canonical SQL: {canonical}\n"
                f"ACTUAL: {json.dumps(actual, indent=2)}\n"
                f"EXPECTED: {json.dumps(expected, indent=2)}"
            )
            passed_test_cases += 1

        print(" [PASS]")

    elapsed = time.time() - start_time
    print(f"\n================================================================================")
    print(f"  RESULTS:")
    print(f"  Total Challenges Verified : {len(ALL_SQL_CHALLENGES)}/53 (100%)")
    print(f"  Total Test Cases Passed   : {passed_test_cases}/{total_test_cases} (100%)")
    print(f"  Execution Time            : {elapsed:.2f}s")
    print(f"  Status                    : ALL CANONICAL SOLUTIONS VALIDATED SUCCESSFULLY!")
    print(f"================================================================================\n")

if __name__ == "__main__":
    run_tests()
