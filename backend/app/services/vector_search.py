import os
import logging
from typing import List, Dict, Any, Tuple
import numpy as np
from app.core.db import get_db

logger = logging.getLogger(__name__)
db = get_db()

# Try to import chromadb
CHROMA_AVAILABLE = False
chroma_client = None
chroma_collection = None

try:
    import chromadb
    # Persistent storage in the workspace
    chroma_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "chroma")
    os.makedirs(chroma_path, exist_ok=True)
    
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    # Use cosine similarity as specified in requirements
    chroma_collection = chroma_client.get_or_create_collection(
        name="face_embeddings", 
        metadata={"hnsw:space": "cosine"}
    )
    CHROMA_AVAILABLE = True
    logger.info("ChromaDB initialized successfully at %s", chroma_path)
except Exception as e:
    logger.warning("ChromaDB initialization failed, falling back to MongoDB + Numpy: %s", e)


class VectorSearchService:
    @staticmethod
    def cosine_similarity_np(v1: List[float], v2: List[float]) -> float:
        """Calculate cosine similarity between two vectors using numpy."""
        arr1 = np.array(v1, dtype=np.float32)
        arr2 = np.array(v2, dtype=np.float32)
        dot = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot / (norm1 * norm2))

    @staticmethod
    async def add_face_embedding(user_id: str, embedding_vector: List[float], angle: str, lighting: str = "normal") -> str:
        """
        Store embedding vector in ChromaDB (if available) and MongoDB for durability/fallback.
        """
        embedding_id = f"{user_id}_{angle}_{int(np.random.randint(1000, 9999))}"
        
        # Save to MongoDB
        await db.face_embeddings.insert_one({
            "userId": user_id,
            "embeddingVector": embedding_vector,
            "angle": angle,
            "lightingCondition": lighting,
            "createdAt": np.datetime64('now').astype(str)
        })
        
        # Save to ChromaDB if available
        if CHROMA_AVAILABLE and chroma_collection:
            try:
                chroma_collection.add(
                    embeddings=[embedding_vector],
                    metadatas=[{"user_id": user_id, "angle": angle, "lighting": lighting}],
                    ids=[embedding_id]
                )
                logger.info("Added face embedding to ChromaDB for user: %s (angle: %s)", user_id, angle)
            except Exception as e:
                logger.error("Failed to add embedding to ChromaDB: %s", e)
                
        return embedding_id

    @staticmethod
    async def search_nearest_neighbors(query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for nearest neighbor face embeddings using Cosine Similarity.
        Attempts ChromaDB search, falls back to raw MongoDB vector similarity calculation.
        """
        # Try ChromaDB
        if CHROMA_AVAILABLE and chroma_collection:
            try:
                results = chroma_collection.query(
                    query_embeddings=[query_vector],
                    n_results=limit
                )
                
                # Format ChromaDB output
                hits = []
                if results and results['ids'] and len(results['ids'][0]) > 0:
                    for i in range(len(results['ids'][0])):
                        user_id = results['metadatas'][0][i]['user_id']
                        # Chroma distance is Cosine Distance (1 - Cosine Similarity)
                        # Let's convert it to Cosine Similarity score (1 - distance)
                        distance = results['distances'][0][i]
                        similarity = 1.0 - distance
                        hits.append({
                            "userId": user_id,
                            "similarity": similarity,
                            "metadata": results['metadatas'][0][i]
                        })
                return hits
            except Exception as e:
                logger.error("ChromaDB query failed, running MongoDB + Numpy fallback: %s", e)
        
        # Fallback: MongoDB + Numpy cosine similarity check
        logger.info("Running Numpy fallback vector similarity search")
        cursor = db.face_embeddings.find({}, {"userId": 1, "embeddingVector": 1, "angle": 1, "lightingCondition": 1})
        all_embeddings = await cursor.to_list(length=1000)
        
        hits = []
        for doc in all_embeddings:
            db_vector = doc.get("embeddingVector")
            if not db_vector:
                continue
            similarity = VectorSearchService.cosine_similarity_np(query_vector, db_vector)
            hits.append({
                "userId": doc["userId"],
                "similarity": similarity,
                "metadata": {
                    "user_id": doc["userId"],
                    "angle": doc.get("angle", "unknown"),
                    "lighting": doc.get("lightingCondition", "normal")
                }
            })
            
        # Sort by similarity descending
        hits.sort(key=lambda x: x["similarity"], reverse=True)
        return hits[:limit]

    @staticmethod
    async def get_average_embedding(user_id: str) -> List[float] | None:
        """
        Average all stored embeddings for a user to create a robust identity profile representation.
        """
        cursor = db.face_embeddings.find({"userId": user_id}, {"embeddingVector": 1})
        docs = await cursor.to_list(length=100)
        
        if not docs:
            return None
            
        vectors = [doc["embeddingVector"] for doc in docs]
        avg_vector = np.mean(vectors, axis=0).tolist()
        return avg_vector

    @staticmethod
    async def delete_user_embeddings(user_id: str):
        """Delete all face embeddings for a user."""
        await db.face_embeddings.delete_many({"userId": user_id})
        
        if CHROMA_AVAILABLE and chroma_collection:
            try:
                chroma_collection.delete(where={"user_id": user_id})
                logger.info("Deleted embeddings in ChromaDB for user %s", user_id)
            except Exception as e:
                logger.error("Failed to delete embeddings in ChromaDB: %s", e)
