from fastapi import APIRouter, Depends, HTTPException, status,Body
from datetime import datetime
from app.auth.jwt_handler import get_current_user
from app.user.utils import user_helper
from app.database import get_db
from app.user.models import VerificationRequest

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


@user_router.post("/verification-request", response_model=dict)
async def submit_verification_request(
        request_data: VerificationRequest = Body(...),
        current_user: dict = Depends(get_current_user)
):
    """
    Submit a verification request
    """
    db = await get_db()

    # Check if there's a pending verification request
    existing_request = await db["VerificationRequests"].find_one({
        "user_id": current_user["id"],
        "status": "pending"
    })

    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending verification request"
        )

    # Create verification request
    verification_request = {
        "user_id": current_user["id"],
        "user_email": current_user["email"],
        "user_name": f"{current_user['first_name']} {current_user['last_name']}",
        "address": request_data.address,
        "id_front_image": request_data.id_front_image,
        "id_back_image": request_data.id_back_image,
        "about_user_article_link": request_data.about_user_article_link,
        "status": "pending",
        "request_date": datetime.utcnow(),
    }

    # Insert verification request into database
    result = await db["VerificationRequests"].insert_one(verification_request)

    return {
        "message": "Verification request submitted successfully",
        "request_id": str(result.inserted_id)
    }


@user_router.get("/verification-requests", response_model=list)
async def get_verification_requests(current_user: dict = Depends(get_current_user)):
    """
    Get all verification requests for a user
    """
    db = await get_db()

    # Get all verification requests for the user
    cursor = db["VerificationRequests"].find(
        {"user_id": current_user["id"]}
    ).sort("request_date", -1)  # Sort by request_date in descending order

    verification_requests = []
    async for request in cursor:
        # Convert ObjectId to string
        request["id"] = str(request["_id"])
        del request["_id"]

        # Format request_date
        if "request_date" in request:
            request["request_date"] = request["request_date"].strftime("%Y-%m-%d %H:%M:%S")

        verification_requests.append(request)

    return verification_requests