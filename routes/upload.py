from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from google.cloud import storage
import os, uuid

router = APIRouter()

bucket_name = os.getenv("GCS_BUCKET")
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

@router.post("/")
async def upload_photo(file: UploadFile = File(...), caption: str = Form(None)):
    try:
        blob_name = f"{uuid.uuid4()}-{file.filename}"
        blob = bucket.blob(blob_name)
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()
        return {"url": blob.public_url, "caption": caption}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
