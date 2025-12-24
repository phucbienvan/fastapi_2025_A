from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import verify_password, oauth2_scheme
from app.db.base import get_db
from app.models.user_model import User
from app.schemas.jwt_schema import Token
from app.services.jwt_service import create_access_token, decode_access_token


def get_user(email: str, db: Session) -> User | None:  
    user = db.query(User).filter(User.email == email).first()
    return user

def authenticate_user(email: str, password: str, db: Session) -> Token:
    user = get_user(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return Token(access_token=access_token, token_type="bearer")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # decode_access_token raises HTTPException if invalid
    token_data = decode_access_token(token)
    
    if token_data.email is None:
        raise credentials_exception
    user = get_user(token_data.email, db)
    if user is None:
        raise credentials_exception
    return user