import hashlib
import json
import logging
from datetime import datetime
from bson.json_util import dumps, loads
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGO_URI, DB_NAME

logger = logging.getLogger(__name__)

if not MONGO_URI or not DB_NAME:
    raise RuntimeError("MONGO_URI or DB_NAME not set in environment")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


class CachedCursor:
    def __init__(self, collection_proxy, raw_cursor, filter_query, *args, **kwargs):
        self._collection_proxy = collection_proxy
        self._raw_cursor = raw_cursor
        self._filter = filter_query
        self._args = args
        self._kwargs = kwargs
        self._chain = []
        self._cached_results = None
        self._index = 0

    def sort(self, *args, **kwargs):
        self._raw_cursor.sort(*args, **kwargs)
        self._chain.append(("sort", args, kwargs))
        return self

    def limit(self, *args, **kwargs):
        self._raw_cursor.limit(*args, **kwargs)
        self._chain.append(("limit", args, kwargs))
        return self

    def skip(self, *args, **kwargs):
        self._raw_cursor.skip(*args, **kwargs)
        self._chain.append(("skip", args, kwargs))
        return self

    async def _fetch_all(self):
        if self._cached_results is not None:
            return self._cached_results

        cache_key = self._collection_proxy._make_key(
            "find_all",
            self._filter,
            self._args,
            self._kwargs,
            self._chain
        )

        async def fetch_from_db():
            results = []
            async for doc in self._raw_cursor:
                results.append(doc)
            return results

        self._cached_results = await self._collection_proxy._cache_get_or_set(
            cache_key,
            fetch_from_db
        )
        self._index = 0
        return self._cached_results

    def __aiter__(self):
        return self

    async def __anext__(self):
        results = await self._fetch_all()
        if self._index >= len(results):
            raise StopAsyncIteration
        val = results[self._index]
        self._index += 1
        return val

    async def to_list(self, length, *args, **kwargs):
        cache_key = self._collection_proxy._make_key(
            "find_to_list",
            self._filter,
            self._args,
            self._kwargs,
            self._chain,
            length
        )

        async def fetch_from_db():
            return await self._raw_cursor.to_list(length, *args, **kwargs)

        return await self._collection_proxy._cache_get_or_set(
            cache_key,
            fetch_from_db
        )


class CachedCollection:
    def __init__(self, raw_collection, name, redis_client):
        self._raw = raw_collection
        self._name = name
        self._redis = redis_client

    def _make_key(self, method, *args):
        serialized = dumps(args)
        h = hashlib.md5(serialized.encode()).hexdigest()
        return f"mongo:{self._name}:{method}:{h}"

    async def _get_version(self):
        try:
            ver = await self._redis.get(f"version:{self._name}")
            if ver is None:
                return "0"
            return ver.decode() if isinstance(ver, bytes) else str(ver)
        except Exception as e:
            logger.warning("Redis error fetching version for %s: %s", self._name, e)
            return "0"

    async def _increment_version(self):
        try:
            await self._redis.incr(f"version:{self._name}")
        except Exception as e:
            logger.error("Failed to increment version for %s: %s", self._name, e)

    async def _cache_get_or_set(self, key_suffix, fetch_func, ttl=300):
        if not self._redis:
            return await fetch_func()

        version = await self._get_version()
        full_key = f"cache:{version}:{key_suffix}"

        try:
            cached = await self._redis.get(full_key)
            if cached is not None:
                logger.debug("Redis HIT for key %s", full_key)
                return loads(cached.decode() if isinstance(cached, bytes) else cached)
        except Exception as e:
            logger.warning("Redis read error on %s: %s", full_key, e)

        logger.debug("Redis MISS for key %s, querying MongoDB", full_key)
        result = await fetch_func()

        try:
            serialized = dumps(result)
            await self._redis.set(full_key, serialized, ex=ttl)
        except Exception as e:
            logger.warning("Redis write error on %s: %s", full_key, e)

        return result

    # --- Read operations ---
    async def find_one(self, filter=None, *args, **kwargs):
        if filter is None:
            filter = {}
        key = self._make_key("find_one", filter, args, kwargs)
        return await self._cache_get_or_set(
            key,
            lambda: self._raw.find_one(filter, *args, **kwargs)
        )

    def find(self, filter=None, *args, **kwargs):
        if filter is None:
            filter = {}
        raw_cursor = self._raw.find(filter, *args, **kwargs)
        return CachedCursor(self, raw_cursor, filter, *args, **kwargs)

    async def count_documents(self, filter, *args, **kwargs):
        key = self._make_key("count_documents", filter, args, kwargs)
        return await self._cache_get_or_set(
            key,
            lambda: self._raw.count_documents(filter, *args, **kwargs)
        )

    async def distinct(self, key_name, filter=None, *args, **kwargs):
        if filter is None:
            filter = {}
        key = self._make_key("distinct", key_name, filter, args, kwargs)
        return await self._cache_get_or_set(
            key,
            lambda: self._raw.distinct(key_name, filter, *args, **kwargs)
        )

    # --- Write operations ---
    async def insert_one(self, *args, **kwargs):
        res = await self._raw.insert_one(*args, **kwargs)
        await self._increment_version()
        return res

    async def insert_many(self, *args, **kwargs):
        res = await self._raw.insert_many(*args, **kwargs)
        await self._increment_version()
        return res

    async def update_one(self, *args, **kwargs):
        res = await self._raw.update_one(*args, **kwargs)
        await self._increment_version()
        return res

    async def update_many(self, *args, **kwargs):
        res = await self._raw.update_many(*args, **kwargs)
        await self._increment_version()
        return res

    async def replace_one(self, *args, **kwargs):
        res = await self._raw.replace_one(*args, **kwargs)
        await self._increment_version()
        return res

    async def delete_one(self, *args, **kwargs):
        res = await self._raw.delete_one(*args, **kwargs)
        await self._increment_version()
        return res

    async def delete_many(self, *args, **kwargs):
        res = await self._raw.delete_many(*args, **kwargs)
        await self._increment_version()
        return res

    async def find_one_and_update(self, *args, **kwargs):
        res = await self._raw.find_one_and_update(*args, **kwargs)
        await self._increment_version()
        return res

    async def find_one_and_delete(self, *args, **kwargs):
        res = await self._raw.find_one_and_delete(*args, **kwargs)
        await self._increment_version()
        return res

    async def find_one_and_replace(self, *args, **kwargs):
        res = await self._raw.find_one_and_replace(*args, **kwargs)
        await self._increment_version()
        return res

    async def bulk_write(self, *args, **kwargs):
        res = await self._raw.bulk_write(*args, **kwargs)
        await self._increment_version()
        return res

    def __getattr__(self, name):
        return getattr(self._raw, name)


class CachedDatabase:
    def __init__(self, raw_db, redis_client):
        self._raw = raw_db
        self._redis = redis_client
        self._collections = {}

    def __getitem__(self, name):
        if name not in self._collections:
            self._collections[name] = CachedCollection(self._raw[name], name, self._redis)
        return self._collections[name]

    def __getattr__(self, name):
        if name.startswith('_'):
            return getattr(self._raw, name)
        return self[name]


_cached_db = None


def get_db():
    global _cached_db
    if _cached_db is None:
        try:
            from app.engine.queue.redis_queue import get_redis_client
            redis_client = get_redis_client()
            _cached_db = CachedDatabase(db, redis_client)
        except Exception as e:
            logger.warning("Failed to initialize CachedDatabase proxy, falling back to raw MongoDB: %s", e)
            return db
    return _cached_db
