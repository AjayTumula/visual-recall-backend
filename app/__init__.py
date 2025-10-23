import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from google.cloud import storage

# Load .env
load_dotenv()

# Firebase Admin
# firebase_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
# cred = credentials.Certificate(firebase_path)
# firebase_admin.initialize_app(cred)
if not firebase_admin._apps:
    firebase_admin.initialize_app()
print("✅ Firebase Admin initialized (no service account)")
print("✅ Firebase Admin initialized")

# Google Cloud Storage
gcs_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcs_path
storage_client = storage.Client()
print("✅ Google Cloud Storage client initialized")
