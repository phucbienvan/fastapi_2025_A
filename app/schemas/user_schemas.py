from pydantic import BaseModel, ConfigDict
from pydantic import field_validator
import re

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    email: str
    status: int

class RegisterUserSchema(BaseModel):
    name: str
    email: str
    password: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, email: str):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('Invalid email address')
        return email

    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return password

class LoginUserSchema(BaseModel):
    email: str
    password: str
    
class LoginUserResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class TokenPayload(BaseModel):
    user_id: int
    exp: int
