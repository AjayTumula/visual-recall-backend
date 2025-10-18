from google.cloud import aiplatform
import os

aiplatform.init(project=os.getenv("PROJECT_ID"), location="us-central1")

def embed_text(text: str):
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    return model.get_embeddings([text])[0].values

def embed_image(gcs_uri: str):
    model = aiplatform.ImageEmbeddingModel.from_pretrained("imageembedding-gecko@001")
    return model.get_embeddings([gcs_uri])[0].values
