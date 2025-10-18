# app/utils/auth_utils.py
import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, Header

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def verify_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.replace("Bearer ", "")
    try:
        decoded = auth.verify_id_token(token)
        return decoded["uid"]
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
