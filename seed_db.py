import asyncio
from app.core.db import get_db
from app.data.seed import CHALLENGES

async def main():
    db = get_db()
    for c in CHALLENGES:
        await db.problems.update_one({'slug': c['slug']}, {'$set': c}, upsert=True)
    print('Updated challenges in MongoDB')

asyncio.run(main())
