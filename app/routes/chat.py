from fastapi import APIRouter, Request, HTTPException
from google.cloud import aiplatform
from app.db.elastic_client import es
from app.ai.embeddings import embed_text
import os

router = APIRouter()

project = os.getenv("PROJECT_ID")
location = "us-central1"
aiplatform.init(project=project, location=location)

@router.post("/")
async def chat(request: Request):
    data = await request.json()
    query_text = data.get("q")
    user_id = request.state.user_id

    if not query_text:
        raise HTTPException(status_code=400, detail="Missing query text")

    try:
        # 1️⃣ Embed query
        query_vector = embed_text(query_text)

        # 2️⃣ Retrieve similar memories
        search_query = {
            "size": 5,
            "query": {
                "script_score": {
                    "query": {"term": {"user_id": user_id}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    },
                }
            },
        }

        res = es.search(index="visual-memories", body=search_query)
        top_memories = [hit["_source"] for hit in res["hits"]["hits"]]

        context_text = "\n".join(
            [f"{m['caption']} ({m['image_url']})" for m in top_memories]
        )

        # 3️⃣ Use Gemini to respond naturally
        from vertexai.preview import generative_models

        model = generative_models.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are an AI memory assistant. The user asked: "{query_text}".
        You have these related memories:
        {context_text}

        Answer in a friendly, human-like way, helping the user recall context.
        """

        response = model.generate_content(prompt)
        return {
            "query": query_text,
            "response": response.text,
            "related_memories": top_memories,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
