import asyncio
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load env before any imports
load_dotenv()

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))

from app.core.db import get_db
from app.engine.controllers.submission_controller import EngineSubmissionController
from app.engine.schemas import RunRequest, InlineTestCase
from app.engine.enums import Language, ComparisonMode

async def run_verification():
    db = get_db()
    
    # 1. Fetch all problems
    problems = await db.problems.find({}).to_list(length=1000)
    print(f"Loaded {len(problems)} problems from MongoDB.")
    
    results = []
    
    for idx, p in enumerate(problems, 1):
        slug = p.get("slug")
        title = p.get("title")
        domain = p.get("domain", "Backend")
        exec_mode = p.get("execution_mode", "cli")
        runtime = p.get("runtime", "algorithm")
        
        print(f"[{idx}/{len(problems)}] Verifying {slug} ({domain})...")
        
        # Check if we have an accepted submission
        sub_doc = await db.submissions.find_one({
            "problem_slug": slug,
            "status": "accepted"
        })
        if not sub_doc:
            sub_doc = await db.engine_submissions.find_one({
                "problem_slug": slug,
                "status": "accepted"
            })
            
        # Get test cases
        db_tcs = p.get("test_cases", [])
        inline_tcs = []
        for tc in db_tcs:
            inline_tcs.append(InlineTestCase(
                id=tc.get("id"),
                stdin=tc.get("stdin", ""),
                expected_output=tc.get("expected_output", ""),
                name=tc.get("name"),
                hidden=tc.get("hidden", False),
                verification_script=tc.get("verification_script"),
                files=tc.get("files")
            ))
            
        code = None
        lang = None
        is_accepted_source = False
        
        if sub_doc:
            code = sub_doc.get("source_code") or sub_doc.get("code")
            lang = sub_doc.get("language")
            is_accepted_source = True
            print(f"  -> Found accepted submission in {lang}")
        else:
            # Fall back to starter code
            starter_code = p.get("starter_code", {})
            if starter_code:
                # Pick the first available key
                avail_langs = list(starter_code.keys())
                for al in avail_langs:
                    code_raw = starter_code[al]
                    code = code_raw
                    # Map avail_lang key to Language enum
                    if al in ("javascript", "js", "js_mongodb", "html"):
                        lang = "javascript"
                    elif al in ("python", "py", "py_mongodb"):
                        lang = "python"
                    elif al == "typescript":
                        lang = "typescript"
                    elif al == "go":
                        lang = "go"
                    elif al == "cpp":
                        lang = "cpp"
                    elif al == "rust":
                        lang = "rust"
                    elif al == "java":
                        lang = "java"
                    else:
                        lang = al
                    break
            print(f"  -> Using starter code in {lang}")
            
        if not code or not lang:
            print(f"  ❌ Skipping: No code or language found")
            results.append({
                "slug": slug,
                "title": title,
                "domain": domain,
                "status": "SKIPPED",
                "verdict": "N/A",
                "details": "No source code or starter code available",
                "is_accepted": is_accepted_source
            })
            continue
            
        # Set comparison mode
        comp_mode_str = p.get("comparison_mode", "trimmed").upper()
        try:
            comp_mode = ComparisonMode[comp_mode_str]
        except Exception:
            comp_mode = ComparisonMode.TRIMMED
            
        # Build RunRequest
        try:
            req = RunRequest(
                language=Language(lang),
                code=code,
                test_cases=inline_tcs,
                time_limit=30.0,  # Generous time limit for verification
                memory_limit=512,
                comparison_mode=comp_mode,
                execution_mode=exec_mode,
                runtime=runtime
            )
            
            # Execute
            exec_res = await EngineSubmissionController.create_run(req)
            
            success = exec_res.get("success", False)
            verdict = exec_res.get("verdict", "UNKNOWN")
            
            # Check individual test cases
            tc_results = exec_res.get("testcase_results", [])
            passed_count = sum(1 for tc in tc_results if tc.get("passed", False))
            total_count = len(tc_results)
            
            details = f"Passed {passed_count}/{total_count} test cases"
            if not success:
                details += f" | Error: {exec_res.get('error', 'None')}"
                
            status_char = "✅" if verdict == "ACCEPTED" else ("⚠️" if is_accepted_source else "ℹ️")
            print(f"  {status_char} Verdict: {verdict} ({details})")
            
            results.append({
                "slug": slug,
                "title": title,
                "domain": domain,
                "status": "PASS" if (not is_accepted_source or verdict == "ACCEPTED") else "FAIL",
                "verdict": verdict,
                "details": details,
                "is_accepted": is_accepted_source
            })
            
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            results.append({
                "slug": slug,
                "title": title,
                "domain": domain,
                "status": "ERROR",
                "verdict": "ERROR",
                "details": f"System Exception: {str(e)}",
                "is_accepted": is_accepted_source
            })
            
    # Generate Markdown report
    report_path = Path(__file__).parent.parent / "scratch" / "verification_report.md"
    with open(report_path, "w") as f:
        f.write("# Interleet Execution Verification Report\n\n")
        f.write(f"Generated at: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Summary\n\n")
        
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        errors = sum(1 for r in results if r["status"] == "ERROR")
        skipped = sum(1 for r in results if r["status"] == "SKIPPED")
        
        f.write(f"- **Total Challenges Tested**: {total}\n")
        f.write(f"- **Successful executions/matches**: {passed}\n")
        f.write(f"- **Mismatched accepted solutions**: {failed}\n")
        f.write(f"- **Execution errors (Infrastructure)**: {errors}\n")
        f.write(f"- **Skipped**: {skipped}\n\n")
        
        f.write("## Challenge Detail Table\n\n")
        f.write("| Slug | Domain | Type | Status | Verdict | Details |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in results:
            type_str = "Accepted Solution" if r["is_accepted"] else "Starter Code"
            f.write(f"| {r['slug']} | {r['domain']} | {type_str} | {r['status']} | {r['verdict']} | {r['details']} |\n")
            
    print(f"\nVerification finished. Report saved to {report_path}")

if __name__ == "__main__":
    asyncio.run(run_verification())
