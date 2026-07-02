import asyncio
import pprint
from app.core.db import get_db

async def main():
    db = get_db()
    p = await db.problems.find_one({})
    pprint.pprint(p)

if __name__ == "__main__":
    asyncio.run(main())
