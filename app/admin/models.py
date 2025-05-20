from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class VerificationRequestModel(BaseModel):
    id: str
    user_id: str
    user_email: EmailStr
    user_name: str
    address: str
    id_front_image: str
    id_back_image: str
    about_user_article_link: str
    status: str
    request_date: datetime
    profile_image: str

    class Config:
        schema_extra = {
            "example": {
                "id": "6829f883bb7e3d091bb3abcb",
                "user_id": "680694d44f57793badb91516",
                "user_email": "john.doe@example.com",
                "user_name": "John Doe",
                "address": "123 Main St, City, Country",
                "id_front_image": "base64_encoded_string...",
                "id_back_image": "base64_encoded_string...",
                "about_user_article_link": "https://example.com/about-user",
                "status": "pending",
                "request_date": "2025-05-18T07:46:02.978+00:00",
                "profile_image": "base64_encoded_profile_image..."
            }
        }