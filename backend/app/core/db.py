from __future__ import annotations

from copy import deepcopy
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI, DB_NAME


class InMemoryCursor:
    def __init__(self, docs: list[dict[str, Any]]):
        self.docs = docs

    def __aiter__(self):
        self._index = 0
        return self

    async def __anext__(self):
        if self._index >= len(self.docs):
            raise StopAsyncIteration
        doc = self.docs[self._index]
        self._index += 1
        return deepcopy(doc)

    def sort(self, *_args, **_kwargs):
        return self

    def limit(self, limit: int):
        self.docs = self.docs[:limit]
        return self


class InMemoryResult:
    def __init__(self, inserted_id: str | None = None, deleted_count: int = 0):
        self.inserted_id = inserted_id
        self.deleted_count = deleted_count


class InMemoryCollection:
    def __init__(self):
        self.docs: list[dict[str, Any]] = []

    def _matches(self, doc: dict[str, Any], query: dict[str, Any] | None) -> bool:
        if not query:
            return True
        for key, expected in query.items():
            if key == "$or":
                return any(self._matches(doc, q) for q in expected)
            value = doc.get(key)
            if isinstance(expected, dict):
                if "$in" in expected and value not in expected["$in"]:
                    return False
                if "$ne" in expected and value == expected["$ne"]:
                    return False
                continue
            if value != expected:
                return False
        return True

    def _project(self, doc: dict[str, Any], projection: dict[str, int] | None):
        result = deepcopy(doc)
        if projection and projection.get("_id") == 0:
            result.pop("_id", None)
        return result

    async def find_one(self, query=None, projection=None):
        for doc in self.docs:
            if self._matches(doc, query):
                return self._project(doc, projection)
        return None

    def find(self, query=None, projection=None):
        return InMemoryCursor(
            [self._project(doc, projection) for doc in self.docs if self._matches(doc, query)]
        )

    async def insert_one(self, doc):
        new_doc = deepcopy(doc)
        new_doc.setdefault("_id", new_doc.get("id") or new_doc.get("slug") or str(len(self.docs) + 1))
        self.docs.append(new_doc)
        return InMemoryResult(inserted_id=str(new_doc["_id"]))

    async def update_one(self, query, update):
        doc = await self.find_one(query)
        if not doc:
            return InMemoryResult()
        await self.find_one_and_update(query, update)
        return InMemoryResult()

    async def find_one_and_update(self, query, update, return_document=None):
        for doc in self.docs:
            if self._matches(doc, query):
                if "$set" in update:
                    doc.update(deepcopy(update["$set"]))
                return deepcopy(doc)
        return None

    async def delete_one(self, query):
        before = len(self.docs)
        self.docs = [doc for doc in self.docs if not self._matches(doc, query)]
        return InMemoryResult(deleted_count=before - len(self.docs))


class InMemoryDatabase:
    def __init__(self):
        self._collections: dict[str, InMemoryCollection] = {}

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)
        return self._collections.setdefault(name, InMemoryCollection())

    def __getitem__(self, name: str):
        return self._collections.setdefault(name, InMemoryCollection())

    async def list_collection_names(self):
        return list(self._collections.keys())


if MONGO_URI and DB_NAME:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
else:
    db = InMemoryDatabase()



def get_db():
    return db
