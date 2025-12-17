from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.product_model import Product
from app.schemas.product_schema import ProductSchema, CreateProductSchema, UpdateProductSchema
from app.schemas.base_schema import DataResponse

router = APIRouter()

@router.get("/products", tags=["products"], description="Get all products", response_model=DataResponse[list[ProductSchema]])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.is_deleted == False).all()
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
    product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    return DataResponse.custom_response(code="200", message="Get product by id", data=product)

@router.put("/products/{product_id}", tags=["products"], description="Update a product by id", response_model=DataResponse[ProductSchema])
def update_product(product_id: int, data: UpdateProductSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return DataResponse.custom_response(code="200", message="Update product success", data=product)

@router.delete("/products/soft/{product_id}", tags=["products"], description="Soft delete a product by id", response_model=DataResponse[ProductSchema])
def soft_delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    
    product.is_deleted = True
    db.commit()
    return DataResponse.custom_response(code="200", message="Soft delete product success", data=None)

@router.delete("/products/{product_id}", tags=["products"], description="Delete a product by id", response_model=DataResponse[ProductSchema])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    db.delete(product)
    db.commit()
    return DataResponse.custom_response(code="200", message="Delete product by id", data=None)
