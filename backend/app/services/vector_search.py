import os
import logging
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
from app.core.db import get_db

logger = logging.getLogger(__name__)
db = get_db()

# ── Pinecone initialisation ────────────────────────────────────────────────
PINECONE_AVAILABLE = False
pinecone_index = None

PINECONE_API_KEY   = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "face-embeddings")
PINECONE_CLOUD     = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION    = os.getenv("PINECONE_REGION", "us-east-1")

# ArcFace / geometric fallback embedding dimension
EMBEDDING_DIM = 512

if PINECONE_API_KEY:
    try:
        from pinecone import Pinecone, ServerlessSpec

        pc = Pinecone(api_key=PINECONE_API_KEY)

        # Create index if it doesn't exist yet
        existing = [idx.name for idx in pc.list_indexes()]
        if PINECONE_INDEX_NAME not in existing:
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=EMBEDDING_DIM,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=PINECONE_CLOUD,
                    region=PINECONE_REGION,
                ),
            )
            logger.info("Pinecone: created index '%s'", PINECONE_INDEX_NAME)

        pinecone_index = pc.Index(PINECONE_INDEX_NAME)
        PINECONE_AVAILABLE = True
        logger.info("Pinecone initialised — index '%s'", PINECONE_INDEX_NAME)

    except Exception as e:
        logger.warning(
            "Pinecone initialisation failed — falling back to MongoDB+Numpy: %s", e
        )
else:
    logger.warning(
        "PINECONE_API_KEY not set — face embeddings will use MongoDB+Numpy fallback only"
    )


# ──────────────────────────────────────────────────────────────────────────────

class VectorSearchService:

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def cosine_similarity_np(v1: List[float], v2: List[float]) -> float:
        """Cosine similarity between two vectors using numpy."""
        a1 = np.array(v1, dtype=np.float32)
        a2 = np.array(v2, dtype=np.float32)
        dot  = np.dot(a1, a2)
        n1   = np.linalg.norm(a1)
        n2   = np.linalg.norm(a2)
        if n1 == 0 or n2 == 0:
            return 0.0
        return float(dot / (n1 * n2))

    # ── Write ─────────────────────────────────────────────────────────────────

    @staticmethod
    async def add_face_embedding(
        user_id: str,
        embedding_vector: List[float],
        angle: str,
        lighting: str = "normal",
    ) -> str:
        """
        Store a face embedding in:
          1. Pinecone (primary, cloud-hosted vector DB)
          2. MongoDB  (always, acts as durable backup + numpy fallback)
        """
        embedding_id = f"{user_id}_{angle}_{random.randint(10000, 99999)}"

        # 1. Always save to MongoDB for durability
        await db.face_embeddings.insert_one({
            "userId":           user_id,
            "embeddingVector":  embedding_vector,
            "angle":            angle,
            "lightingCondition": lighting,
            "createdAt":        datetime.utcnow().isoformat(),
        })
        logger.info("MongoDB: saved embedding for user=%s angle=%s", user_id, angle)

        # 2. Upsert into Pinecone
        if PINECONE_AVAILABLE and pinecone_index is not None:
            try:
                pinecone_index.upsert(
                    vectors=[{
                        "id":       embedding_id,
                        "values":   embedding_vector,
                        "metadata": {
                            "user_id":  user_id,
                            "angle":    angle,
                            "lighting": lighting,
                        },
                    }]
                )
                logger.info("Pinecone: upserted embedding id=%s user=%s", embedding_id, user_id)
            except Exception as e:
                logger.error("Pinecone upsert failed: %s", e, exc_info=True)

        return embedding_id

    # ── Search ────────────────────────────────────────────────────────────────

    @staticmethod
    async def search_nearest_neighbors(
        query_vector: List[float],
        limit: int = 5,
        user_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Nearest-neighbour search using cosine similarity.
        Tries Pinecone first, falls back to MongoDB+Numpy.
        """
        # ── Pinecone path ──────────────────────────────────────────────────
        if PINECONE_AVAILABLE and pinecone_index is not None:
            try:
                filter_dict = {}
                if user_id:
                    filter_dict["user_id"] = {"$eq": user_id}
                
                result = pinecone_index.query(
                    vector=query_vector,
                    top_k=limit,
                    include_metadata=True,
                    filter=filter_dict if filter_dict else None,
                )
                hits = []
                for match in result.get("matches", []):
                    # Pinecone cosine score is already similarity (0-1)
                    hits.append({
                        "userId":     match["metadata"]["user_id"],
                        "similarity": float(match["score"]),
                        "metadata":   match["metadata"],
                    })
                if hits:
                    logger.info("Pinecone: returned %d matches", len(hits))
                    return hits
                logger.info("Pinecone: no matches found, falling back to MongoDB")
            except Exception as e:
                logger.error("Pinecone query failed, using MongoDB fallback: %s", e)

        # ── MongoDB + Numpy fallback ───────────────────────────────────────
        logger.info("Running MongoDB+Numpy similarity search")
        query_filter = {}
        if user_id:
            query_filter["userId"] = user_id
            
        cursor = db.face_embeddings.find(
            query_filter,
            {"userId": 1, "embeddingVector": 1, "angle": 1, "lightingCondition": 1},
        )
        all_docs = await cursor.to_list(length=1000)

        hits = []
        for doc in all_docs:
            vec = doc.get("embeddingVector")
            if not vec:
                continue
            sim = VectorSearchService.cosine_similarity_np(query_vector, vec)
            hits.append({
                "userId":     doc["userId"],
                "similarity": sim,
                "metadata": {
                    "user_id":  doc["userId"],
                    "angle":    doc.get("angle", "unknown"),
                    "lighting": doc.get("lightingCondition", "normal"),
                },
            })

        hits.sort(key=lambda x: x["similarity"], reverse=True)
        return hits[:limit]

    # ── Utility ───────────────────────────────────────────────────────────────

    @staticmethod
    async def get_average_embedding(user_id: str) -> Optional[List[float]]:
        """Average all stored embeddings for a user into one representative vector."""
        cursor = db.face_embeddings.find({"userId": user_id}, {"embeddingVector": 1})
        docs   = await cursor.to_list(length=100)
        if not docs:
            return None
        vectors    = [doc["embeddingVector"] for doc in docs]
        avg_vector = np.mean(vectors, axis=0).tolist()
        return avg_vector

    @staticmethod
    async def delete_user_embeddings(user_id: str) -> None:
        """Remove all face embeddings for a user from MongoDB and Pinecone."""

        # MongoDB
        await db.face_embeddings.delete_many({"userId": user_id})
        logger.info("MongoDB: deleted all embeddings for user=%s", user_id)

        # Pinecone — fetch IDs that belong to this user then delete them
        if PINECONE_AVAILABLE and pinecone_index is not None:
            try:
                # List vectors by metadata filter (requires metadata filtering enabled on index)
                # Use a dummy query to find all vectors for this user
                result = pinecone_index.query(
                    vector=[0.0] * EMBEDDING_DIM,
                    top_k=100,
                    include_metadata=True,
                    filter={"user_id": {"$eq": user_id}},
                )
                ids_to_delete = [m["id"] for m in result.get("matches", [])]
                if ids_to_delete:
                    pinecone_index.delete(ids=ids_to_delete)
                    logger.info(
                        "Pinecone: deleted %d vectors for user=%s",
                        len(ids_to_delete),
                        user_id,
                    )
                else:
                    logger.info("Pinecone: no vectors found for user=%s to delete", user_id)
            except Exception as e:
                logger.error("Pinecone delete failed for user=%s: %s", user_id, e, exc_info=True)
