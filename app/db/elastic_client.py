from elasticsearch import Elasticsearch
import os

ELASTIC_URL = os.getenv("ELASTIC_URL")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")

es = Elasticsearch(ELASTIC_URL, api_key=ELASTIC_API_KEY)
