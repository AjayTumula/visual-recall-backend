from fastapi import APIRouter
from app.ai.embeddings import embed_text
from app.db.elastic_client import es

router = APIRouter()

@router.post("/")
async def query(data: dict):
    vector = embed_text(data["q"])
    search_query = {
        "size": 5,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": vector}
                }
            }
        }
    }
    res = es.search(index="visual-memories", body=search_query)
    return {"results": [hit["_source"] for hit in res["hits"]["hits"]]}
    