from fastapi import APIRouter
from app.schemas.user_schemas import RegisterUserSchema, UserSchema, LoginUserSchema, TokenSchema
from app.models.user_model import User
from app.db.base import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.schemas.base_schema import DataResponse
from app.core.security import hash_password, verify_password, create_access_token
router = APIRouter()


@router.post("/register", tags=["users"], description="Register a new user", response_model=DataResponse[UserSchema])
async def register_user(data: RegisterUserSchema, db: Session = Depends(get_db)):
    try:
        password = hash_password(data.password)
        user = User(full_name=data.full_name, email=data.email, password=password)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return DataResponse.custom_response(code="201", message="Register user success", data=user)
    except Exception as e:
        print(f"ERROR Registering: {str(e)}")
        return DataResponse.custom_response(code="500", message=f"Register user failed: {str(e)}", data=None)

@router.post("/login", tags=["users"], description="Login user", response_model=DataResponse[TokenSchema])
async def login_user(data: LoginUserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return DataResponse.custom_response(code="400", message="Email or password is incorrect", data=None)
    
    if not verify_password(data.password, user.password):
        return DataResponse.custom_response(code="400", message="Email or password is incorrect", data=None)
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return DataResponse.custom_response(
        code="200", 
        message="Login successfully", 
        data={
            "access_token": access_token, 
            "token_type": "bearer",
            "user": user
        }
    )

from app.middleware.authenticate import get_current_user

@router.get("/me", tags=["users"], description="Get current user info", response_model=DataResponse[UserSchema])
async def get_me(current_user: User = Depends(get_current_user)):
    return DataResponse.custom_response(code="200", message="Get current user success", data=current_user)


