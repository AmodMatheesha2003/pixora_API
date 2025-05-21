from fastapi.responses import JSONResponse
import httpx

UPLOAD_API_URL = "https://pixora-nft-copyrights-7e3a5bcac7e4.herokuapp.com/upload"
USER_API_URL = "https://pixora-f96ef5c321f5.herokuapp.com/api/user/me"

async def upload_image_to_api(imageBase64: str, name: str):
    json_payload = {
        "imageBase64": imageBase64,
        "name": name
    }
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            upload_response = await client.post(UPLOAD_API_URL, json=json_payload)
            upload_result = upload_response.json()
        return upload_result, None
    except Exception as e:
        return None, JSONResponse(
            content={"error": f"Upload API connection failed: {str(e)}"},
            status_code=502
        )

async def get_user_info_from_api(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            user_response = await client.get(USER_API_URL, headers=headers, follow_redirects=True)
            user_response.raise_for_status()
            user_data = user_response.json()
        return user_data, None
    except Exception as e:
        return None, JSONResponse(
            content={"error": f"User API connection failed: {str(e)}"},
            status_code=502
        )