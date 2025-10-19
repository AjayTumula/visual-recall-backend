from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from firebase_admin import auth

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # ✅ Allow unauthenticated OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)

        # Skip auth for docs, health, etc.
        public_paths = ["/", "/docs", "/openapi.json", "/health", "/status"]
        if any(request.url.path.startswith(p) for p in public_paths):
            return await call_next(request)

        # Check Authorization header for other routes
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse({"error": "Missing Authorization header"}, status_code=401)

        token = authorization.replace("Bearer ", "")
        try:
            decoded_token = auth.verify_id_token(token)
            request.state.user_id = decoded_token["uid"]
        except Exception as e:
            return JSONResponse({"error": f"Invalid token: {e}"}, status_code=401)

        response = await call_next(request)
        return response
