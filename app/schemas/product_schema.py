from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    description: str

    class Config:
        from_attributes = True

class CreateProductSchema(BaseModel):
    name: str
    price: float
    description: str

class UpdateProductSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
