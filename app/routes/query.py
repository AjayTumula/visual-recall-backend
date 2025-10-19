# app/routes/query.py
from fastapi import APIRouter, Depends, HTTPException
from app.ai.embeddings import embed_text
from app.db.elastic_client import es
from app.utils.auth_utils import verify_user

router = APIRouter()

@router.post("/")
async def query_memories(payload: dict, user_id: str = Depends(verify_user)):
    try:
        query_text = payload.get("q", "")
        query_vector = embed_text(query_text)

        query_body = {
            "query": {
                "script_score": {
                    "query": {"term": {"user_id": user_id}},  # ✅ restrict to user
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            },
            "_source": ["caption", "image_url"]
        }

        res = es.search(index="visual-memories", body=query_body)
        results = [
            {
                "caption": hit["_source"]["caption"],
                "url": hit["_source"]["image_url"]
            }
            for hit in res["hits"]["hits"]
        ]

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
