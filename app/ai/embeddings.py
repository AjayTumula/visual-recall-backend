from sentence_transformers import SentenceTransformer
from PIL import Image
import requests
from io import BytesIO

# Load models once at startup (cached after first use)
print("🔄 Loading embedding models... (this may take 1-2 minutes on first run)")

try:
    text_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Text model loaded!")
    
    image_model = SentenceTransformer('clip-ViT-B-32')
    print("✅ Image model loaded!")
    
    print("🎉 All embedding models ready!")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    text_model = None
    image_model = None

def embed_text(text: str):
    """Generate text embeddings locally - FREE"""
    if text_model is None:
        raise Exception("Text model not loaded")
    
    print(f"📝 Embedding text: {text[:50]}...")
    embedding = text_model.encode(text, convert_to_tensor=False)
    print(f"✅ Generated {len(embedding)}-dim embedding")
    return embedding.tolist()

def embed_image(image_url: str):
    """Generate image embeddings from URL - FREE"""
    if image_model is None:
        raise Exception("Image model not loaded")
    
    try:
        if image_url.startswith('http'):
            response = requests.get(image_url, timeout=10)
            img = Image.open(BytesIO(response.content))
        else:
            img = Image.open(image_url)
        
        embedding = image_model.encode(img, convert_to_tensor=False)
        return embedding.tolist()
    except Exception as e:
        print(f"Error embedding image: {e}")
        raise