from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user_model import User
from app.core.security import verify_token

def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chưa đăng nhập"
        )
    
    try:
        token = authorization.split(" ")[1]  # Lấy phần sau "Bearer "
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ"
        )
    
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token hết hạn hoặc không hợp lệ"
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User không tồn tại"
        )
    
    return user
