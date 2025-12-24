from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schemas import RegisterUserSchema, UserSchema, LoginSchema
from app.models.user_model import User
from app.db.base import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.base_schema import DataResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from fastapi.security import OAuth2PasswordRequestForm 

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", tags=["users"], description="Register a new user", response_model=DataResponse[UserSchema])
async def register_user(data: RegisterUserSchema, db: Session = Depends(get_db)):
    password = hash_password(data.password)
    user = User(name=data.name, email=data.email, password=password)
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return DataResponse.custom_response(code="201", message="Register user success", data=user)
    except Exception as e:
        return DataResponse.custom_response(code="500", message="Register user failed", data=None)
@router.post("/login", tags=["users"], description="Login user")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    # Ghi log đăng nhập (có thể thay bằng ghi vào DB nếu cần)
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not user:
        print(f"[{now}] Đăng nhập thất bại: Không tìm thấy user với email {form_data.username}")
        raise HTTPException(status_code=401, detail="Sai email hoặc mật khẩu")

    if not verify_password(form_data.password, user.password):
        print(f"[{now}] Đăng nhập thất bại: Sai mật khẩu cho user {form_data.username}")
        raise HTTPException(status_code=401, detail="Sai email hoặc mật khẩu")

    if user.status != 1:
        print(f"[{now}] Đăng nhập thất bại: Tài khoản {form_data.username} bị khóa hoặc không hoạt động")
        raise HTTPException(status_code=403, detail="Tài khoản bị khóa hoặc không hoạt động")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    print(f"[{now}] Đăng nhập thành công: {form_data.username}")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

