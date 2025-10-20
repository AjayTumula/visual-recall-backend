from fastapi import APIRouter, File, Form, Depends, UploadFile, HTTPException
from app.utils.auth_utils import verify_user
from app.db.mongo_client import memories_collection
from app.ai.embeddings import embed_text, embed_image
import base64
import uuid
from datetime import datetime
from io import BytesIO
from PIL import Image
from typing import Optional

router = APIRouter()

@router.post("/")
async def upload_memory(
    user_id: str = Depends(verify_user),
    file: Optional[UploadFile] = File(None),  # Optional image
    caption: str = Form(""),  # Can be empty
    memory_type: str = Form("mixed"),  # "text", "image", or "mixed"
):
    """
    Upload a memory: text-only, image-only, or both
    """
    if memories_collection is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    # Validate that at least one content type is provided
    if not file and not caption:
        raise HTTPException(status_code=400, detail="Either image or caption must be provided")

    try:
        print(f"📤 Uploading memory: type={memory_type}, has_image={file is not None}, caption_len={len(caption)}")
        
        # Initialize document
        memory_id = str(uuid.uuid4())
        document = {
            "_id": memory_id,
            "user_id": user_id,
            "caption": caption,
            "memory_type": memory_type,  # "text", "image", or "mixed"
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Process image if provided
        if file:
            image_data = await file.read()
            img = Image.open(BytesIO(image_data))
            
            # Resize
            max_size = (1200, 1200)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to base64
            buffered = BytesIO()
            img_format = img.format or "JPEG"
            img = img.convert('RGB')
            img.save(buffered, format=img_format, quality=85)
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            document.update({
                "image_data": image_base64,
                "image_format": img_format,
                "filename": file.filename
            })
            
            print(f"✅ Image processed: {img.size}")
        
        # Generate embeddings based on content
        embeddings = {}
        
        # Text embedding (from caption)
        if caption:
            try:
                text_vector = embed_text(caption)
                embeddings["text_vector"] = text_vector
                print(f"✅ Text embedding generated: {len(text_vector)} dims")
            except Exception as e:
                print(f"⚠️ Text embedding failed: {e}")
                embeddings["text_vector"] = []
        
        # Image embedding (if image provided)
        # Note: For now we'll skip image embeddings or use CLIP for multimodal
        # You can enhance this later with image-to-vector embeddings
        
        document.update(embeddings)
        
        # Save to MongoDB
        await memories_collection.insert_one(document)
        print(f"✅ Saved memory: {memory_id}")
        
        return {
            "memory_id": memory_id,
            "caption": caption,
            "has_image": file is not None,
            "memory_type": memory_type,
            "message": "✅ Memory saved successfully"
        }

    except Exception as e:
        print(f"❌ Upload error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))