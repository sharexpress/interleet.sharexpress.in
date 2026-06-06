"""Run: python sync_pinecone.py"""
import asyncio, os, random, time
from dotenv import load_dotenv
load_dotenv()

PINECONE_API_KEY    = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "face-embeddings")
MONGO_URI           = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME             = os.getenv("DB_NAME", "interleet")

async def run():
    import motor.motor_asyncio as motor
    from pinecone import Pinecone

    client = motor.AsyncIOMotorClient(MONGO_URI)
    db     = client[DB_NAME]

    # 1. Remove duplicate embeddings (keep only first per user+angle)
    all_docs = await db.face_embeddings.find(
        {}, {"_id": 1, "userId": 1, "angle": 1, "createdAt": 1}
    ).sort("createdAt", 1).to_list(1000)

    seen, dups = set(), []
    for d in all_docs:
        key = (d["userId"], d["angle"])
        if key in seen:
            dups.append(d["_id"])
        else:
            seen.add(key)

    if dups:
        result = await db.face_embeddings.delete_many({"_id": {"$in": dups}})
        print(f"Removed {result.deleted_count} duplicate embedding docs")
    else:
        print("No duplicates found")

    # 2. Upload remaining embeddings to Pinecone
    pc    = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)

    docs = await db.face_embeddings.find(
        {}, {"userId": 1, "angle": 1, "embeddingVector": 1, "lightingCondition": 1}
    ).to_list(200)

    print(f"Uploading {len(docs)} embeddings to Pinecone...")

    vectors = []
    for d in docs:
        emb_id = f"{d['userId']}_{d['angle']}_{random.randint(10000, 99999)}"
        vectors.append({
            "id":     emb_id,
            "values": d["embeddingVector"],
            "metadata": {
                "user_id":  d["userId"],
                "angle":    d["angle"],
                "lighting": d.get("lightingCondition", "normal"),
            },
        })

    if vectors:
        index.upsert(vectors=vectors)
        print(f"Upserted {len(vectors)} vectors")

    time.sleep(3)
    stats = index.describe_index_stats()
    print(f"Pinecone total vectors now: {stats['total_vector_count']}")

    # 3. Quick self-similarity test
    if docs:
        test_vec = docs[0]["embeddingVector"]
        result   = index.query(vector=test_vec, top_k=3, include_metadata=True)
        print("Test query results:")
        for m in result.get("matches", []):
            print(f"  score={m['score']:.4f}  user={m['metadata'].get('user_id')}  angle={m['metadata'].get('angle')}")

    client.close()

asyncio.run(run())
print("Done.")
