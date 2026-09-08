#!/usr/bin/env python3
# Copyright 2026 Sharexpress Contributors
"""
seed_sql_curriculum.py
======================
Idempotently seeds and updates all 53 SQL practice challenges across 5 modules
into MongoDB (`interleet.problems`).

Uses `update_one({"slug": slug}, {"$set": doc}, upsert=True)` to guarantee
zero duplicate slugs and full compatibility with existing collections.
"""

import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env variables
backend_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(backend_dir, ".env"))

sys.path.insert(0, backend_dir)
from sql_curriculum import ALL_SQL_CHALLENGES

def get_db():
    mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI") or "mongodb://localhost:27017"
    db_name = os.getenv("DB_NAME") or os.getenv("MONGODB_DB") or "interleet"
    client = MongoClient(mongo_uri)
    return client[db_name]

def seed():
    db = get_db()
    total = len(ALL_SQL_CHALLENGES)
    print("=" * 80)
    print(f"  INTERLEET DATABASE SEEDER: SQL PRACTICE TRACK")
    print(f"  Target Collection: problems | Challenges to upsert: {total}")
    print("=" * 80)

    upserted_count = 0
    modified_count = 0

    for idx, ch in enumerate(ALL_SQL_CHALLENGES, 1):
        slug = ch["slug"]
        title = ch["title"]

        # Ensure required database fields
        payload = dict(ch)
        payload["domain"] = "Databases"
        payload["runtime"] = "database"
        payload["execution_mode"] = "database"

        res = db.problems.update_one(
            {"slug": slug},
            {"$set": payload},
            upsert=True
        )

        if res.upserted_id:
            upserted_count += 1
            action = "INSERTED"
        else:
            modified_count += 1
            action = "UPDATED "

        print(f"[{idx:02d}/{total}] {action} -> {slug.ljust(38)} | {title[:32]}")

    # Verify total count in database
    db_total = db.problems.count_documents({"domain": "Databases"})
    print("=" * 80)
    print(f"  SEEDING COMPLETE:")
    print(f"  - Newly Inserted: {upserted_count}")
    print(f"  - Updated:        {modified_count}")
    print(f"  - Total Database Challenges in 'Databases' domain: {db_total}")
    print("=" * 80)

if __name__ == "__main__":
    seed()
