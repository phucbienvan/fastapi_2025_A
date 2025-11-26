from fastapi import FastAPI
from app.db.base import get_db
from app.db.base import engine
from app.models import Base
from app.routers.product_router import router as product_router
from app.routers.user_router import router as user_router_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CLASS A",
    description="UTE",
)

app.include_router(product_router)
app.include_router(user_router_router)

@app.get("/home")
async def root():
    return {"message": "Hello World class A"}
