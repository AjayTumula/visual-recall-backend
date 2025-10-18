from fastapi import APIRouter, Depends, HTTPException
from app.ai.embeddings import embed_text
from app.db.elastic_client import es
from utils.auth_utils import verify_user

router = APIRouter()

@router.post("/")
async def index_memory(data: dict, user_id: str = Depends(verify_user)):
    try:
        vector = embed_text(data["caption"])
        doc = {
            "user_id": user_id,
            "caption": data["caption"],
            "image_url": data["image_url"],
            "vector": vector,
        }
        es.index(index="visual-memories", document=doc)
        return {"status": "indexed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
