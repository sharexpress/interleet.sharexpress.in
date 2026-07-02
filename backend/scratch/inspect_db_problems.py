import asyncio
from app.core.db import get_db

async def main():
    db = get_db()
    cursor = db.problems.find({})
    async for p in cursor:
        print(f"{p.get('slug')} | {p.get('title')} | {p.get('domain')} | {p.get('difficulty')}")

if __name__ == "__main__":
    asyncio.run(main())
