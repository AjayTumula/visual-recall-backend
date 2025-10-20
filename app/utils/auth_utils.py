from firebase_admin import auth
from fastapi import HTTPException, Header

def verify_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split("Bearer ")[1]

    try:
        decoded = auth.verify_id_token(token)
        return decoded["uid"]  # ✅ Return only UID
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
