#!/usr/bin/env python3
import os
from pymongo import MongoClient

def unlock_everything():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    db = client["interleet"]

    # 1. Set all users to Pro / Premium
    users_res = db.users.update_many(
        {},
        {"$set": {"is_premium": True, "subscription_status": "active", "plan": "Pro"}}
    )
    print(f"Updated {users_res.modified_count} users to Pro/Premium in MongoDB.")

    # 2. Set all problems to Free (is_premium = False)
    problems_res = db.problems.update_many(
        {},
        {"$set": {"is_premium": False}}
    )
    print(f"Updated {problems_res.modified_count} problems to is_premium=False in MongoDB.")

if __name__ == "__main__":
    unlock_everything()
