
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user_model import User
from app.core.config import settings
import jwt
from jwt import InvalidTokenError

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials  = Depends(security), db: Session = Depends(get_db)) -> User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=401, detail = "Invalid token")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credientials")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    
    return user

def authenticate_required(user: User = Depends(get_current_user)):
    return user
