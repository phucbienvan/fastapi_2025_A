from pydantic import BaseModel, ConfigDict
from pydantic import field_validator
import re

class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    password: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValueError('Invalid email address')
        return value
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return password
    
    