from fastapi import APIRouter, Depends, HTTPException
from app.ai.embeddings import embed_text
from app.db.elastic_client import es
from app.utils.auth_utils import verify_user

router = APIRouter()

@router.post("/")
async def index_memory(data: dict, user_id: str = Depends(verify_user)):
    """
    Index a memory (caption + image) into Elasticsearch
    """
    try:
        vector = embed_text(data["caption"])
        doc = {
            "user_id": user_id,
            "caption": data["caption"],
            "image_url": data["image_url"],
            "vector": vector,
            "timestamp": data.get("timestamp"),
        }

        # ✅ Changed from "visual-memories" to "search-visual"
        es.index(index="search-visual", document=doc)
        return {"status": "indexed"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))