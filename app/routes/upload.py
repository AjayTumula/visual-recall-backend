from fastapi import APIRouter, File, Form, Depends, UploadFile, HTTPException
from google.cloud import storage
from utils.auth_utils import verify_user
import os, uuid

router = APIRouter()

# Load bucket info from environment variable
bucket_name = os.getenv("GCS_BUCKET")

# Initialize GCS client
try:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
except Exception as e:
    print("⚠️ GCS init failed:", e)
    bucket = None

@router.post("/")
async def upload_photo(user_id: str = Depends(verify_user),file: UploadFile = File(...), caption: str = Form(None)):
    """
    Upload a photo to Google Cloud Storage
    """
    if not bucket:
        raise HTTPException(status_code=500, detail="GCS bucket not initialized")

    try:
        blob_name = f"{user_id}/{uuid.uuid4()}-{file.filename}"
        blob = bucket.blob(blob_name)
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()

        return {
            "url": blob.public_url,
            "caption": caption,
            "message": "Upload successful"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
