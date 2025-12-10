from pydantic import BaseModel

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
    