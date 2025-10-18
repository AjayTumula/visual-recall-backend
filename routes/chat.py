from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    q: str

@router.post("/")
async def chat(req: ChatRequest):
    # TODO: use Gemini RAG + Elasticsearch hybrid search
    return {"response": f"Placeholder reply for '{req.q}'"}
