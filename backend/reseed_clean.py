#!/usr/bin/env python3
"""
reseed_clean.py
Drops the 'problems' collection and reseeds it fresh from v2 + v3 seed files.
Safe: does NOT touch users, submissions, XP, or any other collection.

Run:  python3 backend/reseed_clean.py
"""
import asyncio
import os
import sys
import json

# Add backend to path so we can import seed modules
sys.path.insert(0, os.path.dirname(__file__))

from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "interleet"

# ─── Import challenges from both seed files ───────────────────────────────────
# We load them manually to avoid running their main() functions
import importlib.util, types

def load_challenges_from(filepath):
    """Load the CHALLENGES list from a seed file without executing it."""
    spec = importlib.util.spec_from_file_location("_seed_module", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHALLENGES

base_dir = os.path.dirname(__file__)
v2_challenges = load_challenges_from(os.path.join(base_dir, "seed_challenges_v2.py"))
v3_challenges = load_challenges_from(os.path.join(base_dir, "seed_challenges_v3.py"))

# Merge: v3 takes priority (upsert by slug)
all_by_slug = {}
for c in v2_challenges:
    all_by_slug[c["slug"]] = c
for c in v3_challenges:
    all_by_slug[c["slug"]] = c

ALL_CHALLENGES = list(all_by_slug.values())
print(f"Total unique challenges to seed: {len(ALL_CHALLENGES)}")


async def reseed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    col = db["problems"]

    # ── 1. Drop problems collection ──────────────────────────────────────────
    print("Dropping existing 'problems' collection...")
    await col.drop()
    print("  Dropped.")

    # ── 2. Insert all challenges fresh ───────────────────────────────────────
    inserted = 0
    skipped = 0
    existing = set()

    for challenge in ALL_CHALLENGES:
        slug = challenge.get("slug", "")
        if not slug:
            skipped += 1
            continue

        doc = {
            **challenge,
            "_id": str(uuid4()),
        }

        try:
            await col.insert_one(doc)
            inserted += 1
            print(f"  ✓  {slug}")
        except Exception as e:
            skipped += 1
            print(f"  ✗  {slug}: {e}")

    # ── 3. Create indexes ─────────────────────────────────────────────────────
    await col.create_index("slug", unique=True)
    await col.create_index("domain")
    await col.create_index("difficulty")
    await col.create_index("runtime")

    print(f"\n{'─'*50}")
    print(f"Inserted: {inserted}  |  Skipped: {skipped}")
    print(f"Total in DB: {await col.count_documents({})}")
    print("Reseed complete ✅")

    client.close()


if __name__ == "__main__":
    asyncio.run(reseed())
