from elasticsearch import Elasticsearch
import os

ELASTIC_URL = os.getenv("ELASTIC_URL")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")

try:
    es = Elasticsearch(
        ELASTIC_URL,
        api_key=ELASTIC_API_KEY,
        verify_certs=True,
    )
    print("✅ Connected to Elasticsearch")
except Exception as e:
    print(f"⚠️ Elasticsearch init failed: {e}")
    es = None
