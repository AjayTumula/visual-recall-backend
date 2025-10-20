from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, memories, query, chat
import asyncio

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(memories.router, prefix="/memories", tags=["memories"])
app.include_router(query.router, prefix="/query", tags=["query"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Visual Recall API", "status": "ready"}

@app.get("/health")
def health_check():
    """Check if all services are ready"""
    from app.ai import embeddings
    from app.db.mongo_client import memories_collection
    
    return {
        "mongodb": "connected" if memories_collection is not None else "disconnected",
        "text_model": "ready" if embeddings.text_model is not None else "loading",
        "image_model": "ready" if embeddings.image_model is not None else "loading",
    }

@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("🚀 Visual Recall Backend Starting...")
    print("=" * 60)