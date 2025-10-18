from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload import router as upload_router
from app.routes.query import router as query_router
from app.routes.chat import router as chat_router

app = FastAPI(title="Visual Recall Journal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/upload")
app.include_router(query_router, prefix="/query")
app.include_router(chat_router, prefix="/chat")

@app.get("/")
async def root():
    return {"status": "ok"}
