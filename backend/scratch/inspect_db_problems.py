import asyncio
from app.core.db import get_db

async def main():
    db = get_db()
    cursor = db.problems.find({})
    count = 0
    async for p in cursor:
        count += 1
        print(f"=== Problem #{count}: {p.get('slug')} ===")
        print(f"Title: {p.get('title')}")
        print(f"Domain: {p.get('domain')}")
        print(f"Difficulty: {p.get('difficulty')}")
        print(f"Summary: {p.get('summary')}")
        print(f"Starter Code Keys: {list(p.get('starter_code', {}).keys())}")
        # Print a snippet of starter code
        for lang, code in p.get('starter_code', {}).items():
            print(f"  [{lang} Starter Code Snippet]:")
            print("\n".join(f"    {line}" for line in code.splitlines()[:5]))
        print("-" * 60)
    print(f"Total problems found: {count}")

if __name__ == "__main__":
    asyncio.run(main())
