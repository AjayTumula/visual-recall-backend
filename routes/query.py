from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    q: str

@router.post("/")
async def query(req: QueryRequest):
    # TODO: Vertex AI + Elasticsearch hybrid search
    return {"query": req.q, "results": []}
