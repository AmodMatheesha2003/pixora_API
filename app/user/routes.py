from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.jwt_handler import get_current_user
from app.user.utils import user_helper
from app.database import get_db

user_router = APIRouter()


@user_router.get("/me", response_model=dict)
async def get_user_details(current_user: dict = Depends(get_current_user)):
    """
    Get details of the currently authenticated user
    """
    return user_helper(current_user)


@user_router.get("/{user_id}", response_model=dict)
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get details of a specific user by ID (requires authentication)
    """
    # Only allow users to view their own profile or implement role-based access control
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return user_helper(current_user)