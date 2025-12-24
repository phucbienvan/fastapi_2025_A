from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import SessionLocal
from app.models.user_model import User


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        public_paths = [
            "/users/login",
            "/users/register",
            "/docs",
            "/openapi.json",
            "/redoc",
        ]

        if any(request.url.path.startswith(p) for p in public_paths):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Thiếu token"}
            )

        token = auth_header.replace("Bearer ", "")

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
            if not user_id:
                raise JWTError()

        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token không hợp lệ hoặc đã hết hạn"}
            )

        db: Session = SessionLocal()
        user = db.query(User).filter(User.id == int(user_id)).first()
        db.close()

        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "Người dùng không tồn tại"}
            )

        request.state.user = user
        return await call_next(request)
