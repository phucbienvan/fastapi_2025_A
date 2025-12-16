from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.product_model import Product
from app.schemas.product_schema import ProductSchema, CreateProductSchema, UpdateProductSchema
from app.schemas.base_schema import DataResponse
from datetime import datetime

router = APIRouter()

@router.get("/products", tags=["products"], description="Get all products", response_model=DataResponse[list[ProductSchema]])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return DataResponse.custom_response(code="200", message="get list products", data=products)

@router.post("/products", tags=["products"], description="Create a new product", response_model=DataResponse[ProductSchema])
async def create_product(data: CreateProductSchema, db: Session = Depends(get_db)):
    db_product = Product(**data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return DataResponse.custom_response(code="201", message="Create product page", data=db_product)

@router.get("/products/{product_id}", tags=["products"], description="Get a product by id", response_model=DataResponse[ProductSchema])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.deleted_at.is_(None)).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    return DataResponse.custom_response(code="200", message="Get product by id", data=product)

@router.delete("/products/{product_id}", tags=["products"], description="Delete a product by id", response_model=DataResponse[ProductSchema])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.deleted_at.is_(None)).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    db.delete(product)
    db.commit()
    return DataResponse.custom_response(code="200", message="Delete product by id", data=None)

@router.put("/products/{product_id}", tags=["products"], description="Update product", response_model=DataResponse[ProductSchema])
async def update_product(product_id: int,data: UpdateProductSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.deleted_at.is_(None)).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    update_data = data.dict(exclude_unset=True)
    if not update_data:
        return DataResponse.custom_response(code="400", message="No data to update", data=None)
    for field, value in update_data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return DataResponse.custom_response(code="200", message="Product updated successfully", data=product)

@router.delete("/products/soft-delete/{product_id}", tags=["products"], description="Soft delete a product by id", response_model = DataResponse[ProductSchema])
def soft_delete_product(product_id: int, db: Session  = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.deleted_at.is_(None)).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    product.deleted_at = datetime.utcnow()
    db.commit()
    return DataResponse.custom_response(code="200", message="Soft Delete product by id", data=None)

