from fastapi import APIRouter
from app.schemas.user_schemas import RegisterUserSchema, UserSchema
from app.models.user_model import User
from app.db.base import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.base_schema import DataResponse
from app.core.security import hash_password
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

@router.post("/login", tags=["users"], description="Login")
async def login():
    return {"message": "Login page"}