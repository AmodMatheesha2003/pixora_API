from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

from .models import nft_collection
from .utils import upload_image_to_api, get_user_info_from_api

nft_router = APIRouter()

@nft_router.post("/frontend_upload")
async def frontend_upload(
    imageBase64: str = Form(...),
    name: str = Form(...),
    access_token: str = Form(...),
    art_type: str = Form(...),
    description: str = Form(...),
    price: float = Form(...)
):
    # Step 1: Upload image
    upload_result, upload_error = await upload_image_to_api(imageBase64, name)
    if upload_error:
        return upload_error
    if "error" in upload_result:
        return JSONResponse(content={"upload_result": upload_result}, status_code=400)

    # Step 2: Get user info
    user_data, user_error = await get_user_info_from_api(access_token)
    if user_error:
        return JSONResponse(
            content={
                "error": user_error.body.decode() if hasattr(user_error, "body") else str(user_error),
                "upload_result": upload_result
            },
            status_code=502
        )

    user_id = user_data.get("id")
    if not user_id:
        return JSONResponse(content={
            "error": "Could not retrieve user ID from user API response.",
            "user_api_response": user_data,
            "upload_result": upload_result
        }, status_code=500)

    # Step 3: Find the uploaded NFT
    nft = await nft_collection.find_one({"name": name, "imageBase64": imageBase64})
    if not nft:
        nft = await nft_collection.find_one({"name": name})
        if not nft:
            return JSONResponse(content={
                "error": "Could not find the uploaded NFT in MongoDB.",
                "user_id": user_id,
                "upload_result": upload_result
            }, status_code=404)

    image_id = str(nft.get("_id"))

    # Step 4: Update the NFT with owner info and additional fields
    update_result = await nft_collection.update_one(
        {"_id": nft["_id"]},
        {
            "$set": {
                "art_type": art_type,
                "nft_owner": user_id,
                "description": description,
                "price": price
            }
        }
    )

    return {
        "message": "NFT saved, user validated, and metadata stored",
        "user_id": user_id,
        "image_id": image_id,
        "description": description,
        "art_type": art_type,
        "price": price,
        "upload_result": upload_result,
        "image_name": name,
        "mongo_update": {
            "matched_count": update_result.matched_count,
            "modified_count": update_result.modified_count
        }
    }
