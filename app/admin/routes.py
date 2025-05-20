from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.admin.utils import format_verification_request

admin_router = APIRouter()


@admin_router.get("/verification-requests", response_model=list)
async def get_all_verification_requests():
    """
    Fetch all verification requests without authorization
    """
    db = await get_db()

    cursor = db["VerificationRequests"].find().sort("request_date", -1)  # Sort by request_date descending
    verification_requests = []

    async for request in cursor:
        formatted_request = format_verification_request(request)
        verification_requests.append(formatted_request)

    if not verification_requests:
        raise HTTPException(status_code=404, detail="No verification requests found")

    return verification_requests


@admin_router.get("/pending-verification-requests", response_model=list)
async def get_pending_verification_requests():
    """
    Fetch all pending verification requests
    """
    db = await get_db()

    cursor = db["VerificationRequests"].find({"status": "pending"}).sort("request_date", -1)  # Sort by request_date descending
    verification_requests = []

    async for request in cursor:
        formatted_request = format_verification_request(request)
        verification_requests.append(formatted_request)

    if not verification_requests:
        raise HTTPException(status_code=404, detail="No pending verification requests found")

    return verification_requests


@admin_router.get("/approved-verification-requests", response_model=list)
async def get_approved_verification_requests():
    """
    Fetch all approved verification requests
    """
    db = await get_db()

    cursor = db["VerificationRequests"].find({"status": "approved"}).sort("request_date", -1)  # Sort by request_date descending
    verification_requests = []

    async for request in cursor:
        formatted_request = format_verification_request(request)
        verification_requests.append(formatted_request)

    if not verification_requests:
        raise HTTPException(status_code=404, detail="No approved verification requests found")

    return verification_requests


@admin_router.get("/rejected-verification-requests", response_model=list)
async def get_rejected_verification_requests():
    """
    Fetch all rejected verification requests
    """
    db = await get_db()

    cursor = db["VerificationRequests"].find({"status": "rejected"}).sort("request_date", -1)  # Sort by request_date descending
    verification_requests = []

    async for request in cursor:
        formatted_request = format_verification_request(request)
        verification_requests.append(formatted_request)

    if not verification_requests:
        raise HTTPException(status_code=404, detail="No rejected verification requests found")

    return verification_requests


@admin_router.put("/verification-requests/{request_id}/status")
async def update_verification_request_status(request_id: str, status: str):
    """
    Update the status of a verification request to 'approved' or 'rejected'
    """
    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status. Allowed values are 'approved' or 'rejected'.")

    db = await get_db()

    # Find the verification request by ID
    request = await db["VerificationRequests"].find_one({"_id": ObjectId(request_id)})

    if not request:
        raise HTTPException(status_code=404, detail="Verification request not found")

    if request["status"] != "pending":
        raise HTTPException(status_code=400, detail="Only pending requests can be updated")

    # Update the status
    result = await db["VerificationRequests"].update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"status": status}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update status")

    return {"message": f"Verification request {request_id} status updated to {status}"}