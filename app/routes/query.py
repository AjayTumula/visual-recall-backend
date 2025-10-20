from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.db.mongo_client import memories_collection
from app.ai.embeddings import embed_text
from app.utils.auth_utils import verify_user
import numpy as np
from typing import Optional, List

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    search_mode: str = "semantic"  # "semantic", "keyword", "hybrid"
    memory_types: Optional[List[str]] = None  # Filter by type: ["text", "image", "mixed"]
    limit: int = 10
    date_from: Optional[str] = None
    date_to: Optional[str] = None

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    a = np.array(a)
    b = np.array(b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def keyword_match_score(query: str, caption: str) -> float:
    """Simple keyword matching score"""
    query_words = set(query.lower().split())
    caption_words = set(caption.lower().split())
    
    if not query_words:
        return 0.0
    
    matches = query_words.intersection(caption_words)
    return len(matches) / len(query_words)

@router.post("/")
async def query_memories(
    request: QueryRequest,
    user_id: str = Depends(verify_user)
):
    """
    Advanced memory search with multiple modes:
    - semantic: Uses AI embeddings for meaning-based search
    - keyword: Traditional keyword matching
    - hybrid: Combines both approaches
    """
    if memories_collection is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    try:
        print(f"🔍 Search query: '{request.query}' mode: {request.search_mode}")
        
        # Build MongoDB filter
        mongo_filter = {"user_id": user_id}
        
        # Filter by memory types if specified
        if request.memory_types:
            mongo_filter["memory_type"] = {"$in": request.memory_types}
        
        # Date range filtering
        if request.date_from or request.date_to:
            mongo_filter["timestamp"] = {}
            if request.date_from:
                mongo_filter["timestamp"]["$gte"] = request.date_from
            if request.date_to:
                mongo_filter["timestamp"]["$lte"] = request.date_to
        
        # Fetch memories
        cursor = memories_collection.find(mongo_filter)
        
        results = []
        
        # Generate query embedding for semantic search
        query_vector = None
        if request.search_mode in ["semantic", "hybrid"]:
            try:
                query_vector = embed_text(request.query)
                print(f"✅ Query embedding generated")
            except Exception as e:
                print(f"⚠️ Query embedding failed: {e}")
                if request.search_mode == "semantic":
                    request.search_mode = "keyword"  # Fallback
        
        # Process each memory
        async for doc in cursor:
            score = 0.0
            
            # Semantic search
            if request.search_mode in ["semantic", "hybrid"] and query_vector:
                if doc.get("text_vector") and len(doc["text_vector"]) > 0:
                    semantic_score = cosine_similarity(query_vector, doc["text_vector"])
                    score += semantic_score * (0.7 if request.search_mode == "hybrid" else 1.0)
            
            # Keyword search
            if request.search_mode in ["keyword", "hybrid"]:
                caption = doc.get("caption", "")
                keyword_score = keyword_match_score(request.query, caption)
                score += keyword_score * (0.3 if request.search_mode == "hybrid" else 1.0)
            
            # Only include results with positive scores
            if score > 0:
                # Convert image to data URL if exists
                data_url = None
                if doc.get("image_data"):
                    image_format = doc.get("image_format", "JPEG").lower()
                    image_base64 = doc["image_data"]
                    data_url = f"data:image/{image_format};base64,{image_base64}"
                
                results.append({
                    "memory_id": doc["_id"],
                    "caption": doc.get("caption", ""),
                    "image_url": data_url,
                    "memory_type": doc.get("memory_type", "mixed"),
                    "similarity": float(score),
                    "timestamp": doc.get("timestamp", ""),
                    "filename": doc.get("filename", "")
                })
        
        # Sort by score
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Limit results
        results = results[:request.limit]
        
        print(f"✅ Found {len(results)} results")
        
        return {
            "query": request.query,
            "search_mode": request.search_mode,
            "results": results,
            "total": len(results)
        }

    except Exception as e:
        print(f"❌ Query error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggestions")
async def get_search_suggestions(
    user_id: str = Depends(verify_user),
    limit: int = 5
):
    """
    Get search suggestions based on user's memory captions
    """
    if memories_collection is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        # Get recent memories with captions
        cursor = memories_collection.find(
            {"user_id": user_id, "caption": {"$ne": ""}},
            {"caption": 1}
        ).sort("timestamp", -1).limit(20)
        
        # Extract common words/phrases
        all_words = []
        async for doc in cursor:
            caption = doc.get("caption", "")
            words = caption.lower().split()
            all_words.extend(words)
        
        # Count word frequency
        from collections import Counter
        word_counts = Counter(all_words)
        
        # Filter out common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        suggestions = [
            word for word, count in word_counts.most_common(limit * 2)
            if word not in common_words and len(word) > 3
        ][:limit]
        
        return {"suggestions": suggestions}
        
    except Exception as e:
        print(f"❌ Suggestions error: {e}")
        return {"suggestions": []}