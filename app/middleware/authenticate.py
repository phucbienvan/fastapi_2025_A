from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.security import decode_access_token
from app.db.base import SessionLocal
from sqlalchemy.orm import Session
from app.models.user_model import User


class AuthenticateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        path = request.url.path
        method = request.method.upper()

        protected = path.startswith("/products") and method in {"POST", "PUT", "DELETE"}

        if not protected:
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return JSONResponse({"code": "401", "message": "Missing credentials", "data": None}, status_code=401)

        token = auth.split(" ", 1)[1]
        try:
            payload = decode_access_token(token)
            user_id = payload.get("user_id")
            if not user_id:
                return JSONResponse({"code": "401", "message": "Invalid token", "data": None}, status_code=401)

            # attach user to request.state
            db: Session = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()
                request.state.current_user = user
            finally:
                db.close()
        except Exception:
            return JSONResponse({"code": "401", "message": "Could not validate credentials", "data": None}, status_code=401)

        return await call_next(request)
