import asyncio
import json
from app.core.db import get_db

async def main():
    db = get_db()
    # Get one frontend challenge in full detail
    p = await db.problems.find_one({"slug": "toast-queue-manager"})
    if p:
        p.pop("_id", None)
        print(json.dumps(p, indent=2, default=str))
    
    print("\n\n=== TEST CASES ===")
    cursor = db.test_cases.find({"problem_slug": "toast-queue-manager"})
    async for tc in cursor:
        tc.pop("_id", None)
        print(json.dumps(tc, indent=2, default=str))

asyncio.run(main())
