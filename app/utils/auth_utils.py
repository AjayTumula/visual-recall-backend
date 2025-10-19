from fastapi import Request, HTTPException
from firebase_admin import auth as firebase_auth

def verify_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth_header.split(" ")[1]
    decoded_token = firebase_auth.verify_id_token(token)
    return decoded_token
