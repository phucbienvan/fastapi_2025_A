from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schemas import RegisterUserSchema, UserSchema, LoginSchema
from app.models.user_model import User
from app.db.base import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.base_schema import DataResponse
from app.core.security import hash_password,verify_password, create_access_token
router = APIRouter()


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
    
@router.post("/login", tags=["users"])
async def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Email or password incorrect")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Email or password incorrect")

    access_token = create_access_token(
        data={"user_id": user.id}
    )

    return DataResponse.custom_response(
        code="200",
        message="Login success",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserSchema.model_validate(user)
        }
    )

