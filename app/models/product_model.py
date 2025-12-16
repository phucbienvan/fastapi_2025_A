from app.models.base_model import BaseModel
from sqlalchemy import Boolean, Column, String, Float, DateTime, Integer
import datetime

class Product(BaseModel):
    __tablename__ = "products"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    description: str = Column(String, index=True)
    price: float = Column(Float, index=True)
    created_at: datetime.datetime = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_deleted: bool = Column(Boolean, default=0)
