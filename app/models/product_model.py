from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Float, DateTime, Integer
from datetime import datetime 

class Product(BaseModel):
    __tablename__ = "products"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    description: str = Column(String, index=True)
    price: float = Column(Float, index=True)
    created_at: datetime = Column(
            DateTime,
            default=datetime.utcnow
    )
    updated_at: datetime = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow  
    )
    deleted_at: datetime = Column(
        DateTime,
        nullable=True
    )
