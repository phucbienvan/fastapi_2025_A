from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.product_model import Product

router = APIRouter()

@router.get("/products", tags=["products"], description="Get all products",)
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.post("/products", tags=["products"], description="Create a new product")
async def create_product():
    return {"message": "Create product page"}

@router.put("/products", tags=["products"], description="Update a product")
async def update_product():
    return {"message": "Update product page"}
