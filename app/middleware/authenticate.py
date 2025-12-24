from fastapi import Request, HTTPException
from jose import jwt, JWTError
from app.core.config import settings

async def authenticate_middleware(request: Request, call_next):
    if request.url.path in ["/login", "/register"]:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        request.state.user = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token has expired or is invalid")

    response = await call_next(request)
    return response