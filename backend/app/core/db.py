from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI, DB_NAME


if not MONGO_URI or not DB_NAME:
    raise RuntimeError("MONGO_URI or DB_NAME not set in environment")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


def get_db():
    return db
