from fastapi import APIRouter
from app.ai.embeddings import embed_text
from app.db.elastic_client import es

router = APIRouter()

@router.post("/")
async def index_memory(data: dict):
    doc = {
        "user_id": data["user_id"],
        "caption": data["caption"],
        "image_url": data["image_url"],
        "vector": embed_text(data["caption"])
    }
    es.index(index="visual-memories", document=doc)
    return {"status": "indexed"}
