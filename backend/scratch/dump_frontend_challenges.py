import asyncio
import json
from app.core.db import get_db

async def main():
    db = get_db()
    cursor = db.problems.find({"domain": "Frontend"})
    challenges = []
    async for p in cursor:
        p.pop("_id", None)
        challenges.append(p)
    
    for c in challenges:
        print(f"\n{'='*80}")
        print(f"SLUG: {c.get('slug')}")
        print(f"TITLE: {c.get('title')}")
        print(f"DIFFICULTY: {c.get('difficulty')}")
        print(f"TAGS: {c.get('tags')}")
        print(f"SHORT DESC: {c.get('short_description')}")
        print(f"STARTER_CODE keys: {list(c.get('starter_code', {}).keys())}")
        sc = c.get('starter_code', {})
        for lang, code in sc.items():
            print(f"\n  --- {lang} starter ---")
            print(code[:200])
        print(f"\nTEST_CASES ({len(c.get('test_cases', []))}):")
        for tc in c.get('test_cases', []):
            print(f"  {tc.get('name')}: stdin={tc.get('stdin','')[:80]!r} expected={tc.get('expected_output','')[:80]!r}")

asyncio.run(main())
