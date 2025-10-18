import firebase_admin
from firebase_admin import credentials, auth
import os

cred = credentials.Certificate(os.getenv("C:\Users\ajayt"))
firebase_admin.initialize_app(cred)

def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token["uid"]
    except Exception as e:
        raise Exception(f"Invalid Firebase token: {e}")
