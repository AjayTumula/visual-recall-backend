# app/routes/memories.py
from fastapi import APIRouter, Depends, HTTPException
from app.db.elastic_client import es
from app.utils.auth_utils import verify_user

router = APIRouter()

@router.get("/")
async def get_user_memories(user_id: str = Depends(verify_user)):
    """
    Fetch all memories for the logged-in user
    """
    try:
        query = {
            "query": {
                "term": {"user_id": user_id}
            },
            "sort": [{"_id": {"order": "desc"}}],
            "_source": ["caption", "image_url"]
        }
        res = es.search(index="visual-memories", body=query)
        results = [
            {
                "caption": hit["_source"]["caption"],
                "image_url": hit["_source"]["image_url"],
            }
            for hit in res["hits"]["hits"]
        ]
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
