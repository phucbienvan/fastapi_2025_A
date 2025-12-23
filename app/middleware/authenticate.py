from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_model import User
from app.core.security import verify_password


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Email or password incorrect")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Email or password incorrect")
    return user