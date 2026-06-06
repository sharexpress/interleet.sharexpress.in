"""
Quick diagnostic script — run from the backend/ directory:

  python check_pinecone.py

Shows:
  1. Pinecone index stats (how many vectors total)
  2. All face_embeddings stored in MongoDB
  3. A test similarity between the first two stored embeddings
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY    = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "face-embeddings")
MONGO_URI           = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME             = os.getenv("DB_NAME", "interleet")


# ── 1. Pinecone stats ─────────────────────────────────────────────────────────
def check_pinecone():
    if not PINECONE_API_KEY or PINECONE_API_KEY == "your_pinecone_api_key_here":
        print("❌  PINECONE_API_KEY not set in .env")
        return

    try:
        from pinecone import Pinecone
        pc    = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)
        stats = index.describe_index_stats()
        total = stats.get("total_vector_count", stats.get("totalVectorCount", "?"))
        print(f"✅  Pinecone index '{PINECONE_INDEX_NAME}'")
        print(f"    Total vectors stored : {total}")
        print(f"    Dimension            : {stats.get('dimension', '?')}")

        # Try to fetch any 3 vectors to see what's in there
        print("\n    Sample fetch (up to 3 records via dummy query):")
        try:
            result = index.query(
                vector=[0.0] * 512,
                top_k=3,
                include_metadata=True,
            )
            matches = result.get("matches", [])
            if not matches:
                print("    ⚠️  No matches returned (index may be empty)")
            for m in matches:
                print(f"    id={m['id']}  score={m['score']:.4f}  meta={m.get('metadata')}")
        except Exception as e:
            print(f"    Query error: {e}")

    except Exception as e:
        print(f"❌  Pinecone error: {e}")


# ── 2. MongoDB face_embeddings ────────────────────────────────────────────────
async def check_mongo():
    try:
        import motor.motor_asyncio as motor
        client = motor.AsyncIOMotorClient(MONGO_URI)
        db     = client[DB_NAME]

        docs = await db.face_embeddings.find(
            {}, {"userId": 1, "angle": 1, "createdAt": 1, "_id": 0}
        ).to_list(length=50)

        print(f"\n✅  MongoDB '{DB_NAME}.face_embeddings'")
        print(f"    Total documents: {len(docs)}")
        for d in docs:
            print(f"    user={d.get('userId')}  angle={d.get('angle')}  at={d.get('createdAt')}")

        # Also check users with face_registered=True
        face_users = await db.users.find(
            {"face_registered": True}, {"email": 1, "user_id": 1, "face_registered": 1, "_id": 0}
        ).to_list(length=20)
        print(f"\n    Users with face_registered=True: {len(face_users)}")
        for u in face_users:
            print(f"    email={u.get('email')}  user_id={u.get('user_id')}")

        # Similarity test between first 2 embeddings
        emb_docs = await db.face_embeddings.find({}, {"embeddingVector": 1, "userId": 1, "angle": 1}).to_list(2)
        if len(emb_docs) >= 2:
            import numpy as np
            v1 = np.array(emb_docs[0]["embeddingVector"], dtype=np.float32)
            v2 = np.array(emb_docs[1]["embeddingVector"], dtype=np.float32)
            sim = float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9))
            print(f"\n    Similarity between first 2 stored embeddings: {sim:.4f}")
            print(f"    ({emb_docs[0]['userId']} {emb_docs[0]['angle']} ↔ {emb_docs[1]['userId']} {emb_docs[1]['angle']})")
            if sim > 0.40:
                print("    ✅  Same-user similarity looks good for login (> 0.40 threshold)")
            else:
                print("    ⚠️  Similarity is LOW — embeddings may be inconsistent across frames")

        client.close()
    except Exception as e:
        print(f"❌  MongoDB error: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("  Face ID Diagnostic Tool")
    print("=" * 60)
    check_pinecone()
    asyncio.run(check_mongo())
    print("\nDone.")
