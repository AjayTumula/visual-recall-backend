from fastapi import FastAPI
from app.middleware.auth_middleware import FirebaseAuthMiddleware
from app.routes import upload, index_memory, query, chat

app = FastAPI(title="Visual Recall Journal API")
app.add_middleware(FirebaseAuthMiddleware)

app.include_router(upload.router, prefix="/upload")
app.include_router(index_memory.router, prefix="/index_memory")
app.include_router(query.router, prefix="/query")
app.include_router(chat.router, prefix="/chat")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
