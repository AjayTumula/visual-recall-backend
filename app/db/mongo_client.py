from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGO_DB", "visual_recall")

# Initialize async MongoDB client
try:
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DATABASE_NAME]
    memories_collection = db["memories"]
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"⚠️ MongoDB init failed: {e}")
    db = None
    memories_collection = None