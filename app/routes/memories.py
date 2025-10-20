from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from app.db.mongo_client import memories_collection
from app.utils.auth_utils import verify_user
import base64

router = APIRouter()

@router.get("/")
async def get_user_memories(user_id: str = Depends(verify_user)):
    """
    Fetch all memories for the logged-in user from MongoDB.
    """
    # ✅ Fix: Compare with None instead of bool()
    if memories_collection is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    try:
        cursor = memories_collection.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(100)
        
        memories = []
        async for doc in cursor:
            image_format = doc.get("image_format", "JPEG").lower()
            image_base64 = doc.get("image_data", "")
            data_url = f"data:image/{image_format};base64,{image_base64}"
            
            memories.append({
                "memory_id": doc["_id"],
                "caption": doc.get("caption", ""),
                "image_url": data_url,
                "timestamp": doc.get("timestamp", ""),
                "filename": doc.get("filename", "")
            })
        
        return {
            "memories": memories,
            "count": len(memories)
        }

    except Exception as e:
        print(f"Fetch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))