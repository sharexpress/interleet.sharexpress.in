#!/usr/bin/env python3
import json, urllib.request

resp = urllib.request.urlopen("http://localhost:8001/challenges")
data = json.loads(resp.read())
challenges = data.get("data", [])

print(f"\n{'='*70}")
print(f"  CHALLENGES API QA REPORT  (Total: {data.get('total')})")
print(f"{'='*70}")

issues = []

REQUIRED_DOMAINS = {"Frontend", "Backend", "DevOps", "APIs", "Databases", "Fullstack"}
seen_domains = set()

for c in challenges:
    slug = c.get("slug", "?")
    domain = c.get("domain", "?")
    runtime = c.get("runtime")
    rc = c.get("runtime_config")
    sc = c.get("starter_code") or {}
    tc = c.get("test_cases") or []
    
    seen_domains.add(domain)
    rc_ok = bool(rc)
    has_js = any("js" in k or "javascript" in k or "html" in k or "multi" in k for k in sc.keys())
    has_py = any("py" in k or "python" in k for k in sc.keys())
    has_tests = len(tc) > 0
    execution_mode = c.get("execution_mode", "?")
    
    status = "✓" if (rc_ok and has_tests) else "✗"
    print(f"\n  {status} [{domain[:5]}] {slug}")
    print(f"    runtime={runtime} | exec_mode={execution_mode}")
    print(f"    runtime_config={'PRESENT ✓' if rc_ok else 'MISSING ✗'}")
    print(f"    starter_code keys: {list(sc.keys())}")
    print(f"    has_python: {'✓' if has_py else '✗ MISSING'}  |  has_js: {'✓' if has_js else '✗ MISSING'}")
    print(f"    test_cases: {len(tc)} {'✓' if has_tests else '✗ NONE'}")

    if not rc_ok and execution_mode not in ("essay", None):
        issues.append(f"  ✗ {slug}: runtime_config MISSING (runtime={runtime})")
    if not has_tests and execution_mode not in ("essay",):
        issues.append(f"  ✗ {slug}: no test_cases defined")
    if not has_js and execution_mode not in ("essay",):
        issues.append(f"  ✗ {slug}: no JavaScript starter code")

missing_domains = REQUIRED_DOMAINS - seen_domains
print(f"\n{'='*70}")
print(f"  MISSING DOMAINS: {missing_domains or 'None ✓'}")
print(f"  TOTAL: {len(challenges)} challenges")
print(f"\n  ISSUES FOUND ({len(issues)}):")
for i in issues:
    print(i)

print(f"\n  QA STATUS: {'PASS ✓' if not issues and not missing_domains else 'FAIL ✗'}")
print(f"{'='*70}\n")
