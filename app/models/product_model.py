from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Float, DateTime, Integer
from datetime import datetime, timezone

class Product(BaseModel):
    __tablename__ = "products"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    description: str = Column(String, index=True)
    price: float = Column(Float, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
