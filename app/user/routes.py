from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Body
from datetime import datetime
from app.auth.jwt_handler import get_current_user
from app.user.models import VerificationRequestInput, UpdateUserProfile
from app.user.utils import user_helper, user_details_helper
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


@user_router.post("/verification-request", response_model=dict)
async def submit_verification_request(
        request_data: VerificationRequestInput = Body(...),
        current_user: dict = Depends(get_current_user)
):
    """
    Submit a verification request
    """
    db = await get_db()

    # Get user ID, checking both possible keys
    if "_id" in current_user:
        user_id = str(current_user["_id"])
    elif "id" in current_user:
        user_id = current_user["id"]
    else:
        # Print available keys for debugging
        print(f"Available keys in current_user: {current_user.keys()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not determine user ID"
        )

    # Check if there's a pending verification request
    existing_request = await db["VerificationRequests"].find_one({
        "user_id": user_id,
        "status": "pending"
    })

    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending verification request"
        )

    # Create verification request
    verification_request = {
        "user_id": user_id,
        "user_email": current_user.get("email", ""),
        "user_name": f"{current_user.get('first_name', '')} {current_user.get('last_name', '')}",
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


@user_router.get("/verification-requests", response_description="Get all verification requests for the current user")
async def get_verification_requests(current_user: dict = Depends(get_current_user)):
    """
    Get all verification requests for the current user
    """
    # Get the database connection
    db = await get_db()

    # Get user ID from the current user (as string)
    user_id = current_user["id"]

    print(f"Current user: {current_user}")
    print(f"Looking for verification requests with user_id: {user_id}")

    # First check if there are ANY verification requests in the collection
    all_requests_count = await db["VerificationRequests"].count_documents({})
    print(f"Total documents in VerificationRequests collection: {all_requests_count}")

    # Try to find ALL verification requests first
    all_requests = []
    async for doc in db["VerificationRequests"].find().limit(5):
        print(f"Sample document: {doc}")
        if "user_id" in doc:
            print(f"Sample user_id: {doc['user_id']} (type: {type(doc['user_id']).__name__})")
        all_requests.append(doc)

    print(f"Sample of {len(all_requests)} documents from collection")

    # Now try different ways to find documents for this specific user

    # 1. Try exact match
    cursor = db["VerificationRequests"].find({"user_id": user_id})

    verification_requests = []
    async for request in cursor:
        # Keep a copy of the original document for inspection
        request_copy = dict(request)

        # Add a string id for API response
        request_copy["id"] = str(request["_id"])

        # Format date if needed
        if "request_date" in request_copy and isinstance(request_copy["request_date"], datetime):
            request_copy["request_date"] = request_copy["request_date"].strftime("%Y-%m-%d %H:%M:%S")

        verification_requests.append(request_copy)

    print(f"Found {len(verification_requests)} verification requests for user_id: {user_id}")

    # If nothing found, try a more flexible approach
    if not verification_requests and all_requests:
        print("Trying more flexible match...")
        # This is a diagnostic step to see if we can find the user's requests with different approaches
        for doc in all_requests:
            if "user_id" in doc and doc["user_id"] == user_id:
                print(f"Found match with exact string comparison!")
            elif "user_id" in doc and str(doc["user_id"]) == user_id:
                print(f"Found match after converting to string!")

    # Return whatever we found
    return verification_requests


@user_router.get("/users/me", response_model=dict)
async def get_logged_in_user_details(current_user: dict = Depends(get_current_user)):
    """
    Fetch the logged-in user's details
    """
    return user_details_helper(current_user)

@user_router.put("/me/profile", response_model=dict)
async def update_user_profile(
    update_data: UpdateUserProfile = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Update the first name, last name, and bio of the currently authenticated user
    """
    db = await get_db()

    # Update the user's first_name, last_name, and bio in the database
    result = await db["users"].update_one(
        {"_id": current_user["id"]},  # Filter by user ID
        {
            "$set": {
                "first_name": update_data.first_name,
                "last_name": update_data.last_name,
                "contact": update_data.contact,
                "profile_image": update_data.profile_image,
                "cover_image": update_data.cover_image,
                "bio": update_data.bio,
                "facebook": update_data.facebook,
                "instagram": update_data.instagram,
                "twitter": update_data.twitter,
                "linkedin": update_data.linkedin
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update the user profile"
        )

    # Return the updated fields
    return {
        "message": "Profile updated successfully"
    }