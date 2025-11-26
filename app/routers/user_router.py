from fastapi import APIRouter

router = APIRouter()

@router.get("/users", tags=["users"], description="Get all users")
async def get_users():
    return {"message": "Users page"}

@router.post("/users", tags=["users"], description="Create a new user")
async def create_user():
    return {"message": "Create user page"}

@router.put("/users", tags=["users"], description="Update a user")
async def update_user():
    return {"message": "Update user page"}

@router.delete("/users", tags=["users"], description="Delete a user")
async def delete_user():
    return {"message": "Delete user page"}
