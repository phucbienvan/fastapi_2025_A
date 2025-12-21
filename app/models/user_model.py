from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Float, DateTime, Integer
from datetime import datetime

class User(BaseModel):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    email: str = Column(String, index=True)
    password: str = Column(String, index=True)
    status: int = Column(Integer, index=True, default=1)
    created_at: datetime = Column(DateTime, index=True, default=datetime.now)
    updated_at: datetime = Column(DateTime, index=True, default=datetime.now)
