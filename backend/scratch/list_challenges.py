import asyncio
from app.core.db import get_db

async def main():
    db = get_db()
    cursor = db.problems.find({})
    async for p in cursor:
        slug = p.get("slug", "")
        title = p.get("title", "")
        domain = p.get("domain", "")
        difficulty = p.get("difficulty", "")
        tags = p.get("tags", [])
        print(f"{slug} | {title} | {domain} | {difficulty} | {tags}")
    print("---")
    count = await db.problems.count_documents({})
    front_count = await db.problems.count_documents({"domain": "Frontend"})
    print(f"Total: {count}, Frontend: {front_count}")

asyncio.run(main())
