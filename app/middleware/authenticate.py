from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user_model import User
from app.core.config import settings
from app.schemas.base_schema import DataResponse

oauth2_scheme = APIKeyHeader(name="Authorization", auto_error=False)

from fastapi import Depends, HTTPException, status

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception

    try:
        actual_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
        payload = jwt.decode(actual_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user
