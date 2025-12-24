from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings
import jwt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_id: int) -> str:
    expired = datetime.now() + timedelta(minutes=30)
    payload = {
        "user_id": user_id,
        "exp": int(expired.timestamp())
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
    return token
