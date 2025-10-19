from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.auth_middleware import FirebaseAuthMiddleware
from app.routes import upload, index_memory, query, chat, memories

app = FastAPI(title="Visual Recall Journal API")

# Firebase Authentication Middleware (run first)
app.add_middleware(FirebaseAuthMiddleware)

# ✅ CORS middleware should be added last so its headers are always set
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(index_memory.router, prefix="/index_memory", tags=["Index"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(memories.router, prefix="/memories", tags=["Memories"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
