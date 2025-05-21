from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from typing import Optional, List
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    REGULAR = "regular"
    ARTIST = "artist"
    ADMIN = "admin"


class SocialMediaLinks(BaseModel):
    twitter: Optional[HttpUrl] = None
    instagram: Optional[HttpUrl] = None
    facebook: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None
    other: Optional[HttpUrl] = None


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    profile_image_url: Optional[HttpUrl] = None
    cover_image_url: Optional[HttpUrl] = None
    social_media: Optional[SocialMediaLinks] = None
    notification_preferences: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Doe",
                "bio": "Digital artist specializing in abstract art",
                "profile_image_url": "https://example.com/profile.jpg",
                "cover_image_url": "https://example.com/cover.jpg",
                "social_media": {
                    "twitter": "https://twitter.com/johndoe",
                    "instagram": "https://instagram.com/johndoe"
                },
                "notification_preferences": {
                    "email_notifications": True,
                    "sale_alerts": True,
                    "auction_updates": True
                }
            }
        }


class UserPublicProfile(BaseModel):
    id: str
    username: str
    full_name: str
    bio: Optional[str] = None
    profile_image_url: Optional[HttpUrl] = None
    cover_image_url: Optional[HttpUrl] = None
    role: UserRole
    is_verified_artist: bool
    social_media: Optional[SocialMediaLinks] = None
    created_at: datetime
    artworks_count: int = 0

    class Config:
        schema_extra = {
            "example": {
                "id": "user123",
                "username": "johndoe",
                "full_name": "John Doe",
                "bio": "Digital artist specializing in abstract art",
                "profile_image_url": "https://example.com/profile.jpg",
                "cover_image_url": "https://example.com/cover.jpg",
                "role": "artist",
                "is_verified_artist": True,
                "social_media": {
                    "twitter": "https://twitter.com/johndoe",
                    "instagram": "https://instagram.com/johndoe"
                },
                "created_at": "2025-01-01T00:00:00Z",
                "artworks_count": 15
            }
        }


class UserPrivateProfile(UserPublicProfile):
    email: EmailStr
    notification_preferences: Optional[dict] = None
    wallet_address: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "user123",
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "bio": "Digital artist specializing in abstract art",
                "profile_image_url": "https://example.com/profile.jpg",
                "cover_image_url": "https://example.com/cover.jpg",
                "role": "artist",
                "is_verified_artist": True,
                "social_media": {
                    "twitter": "https://twitter.com/johndoe",
                    "instagram": "https://instagram.com/johndoe"
                },
                "created_at": "2025-01-01T00:00:00Z",
                "artworks_count": 15,
                "notification_preferences": {
                    "email_notifications": True,
                    "sale_alerts": True,
                    "auction_updates": True
                },
                "wallet_address": "0x1234567890abcdef1234567890abcdef12345678"
            }
        }



# Define the verification status as an enum for better type safety
class VerificationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# Input model - what user submits when creating a verification request
class VerificationRequestInput(BaseModel):
    address: str = Field(..., description="User's physical address")
    id_front_image: str = Field(..., description="Base64 encoded image of ID front")
    id_back_image: str = Field(..., description="Base64 encoded image of ID back")
    about_user_article_link: HttpUrl = Field(..., description="Link to an article about the user")

    class Config:
        json_schema_extra = {
            "example": {
                "address": "123 Main St, City, Country",
                "id_front_image": "base64_encoded_string...",
                "id_back_image": "base64_encoded_string...",
                "about_user_article_link": "https://example.com/about-user"
            }
        }


# Database model - the complete verification request as stored in DB
class VerificationRequestInDB(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="Verification request ID")
    user_id: str = Field(..., description="ID of the user who submitted the request")
    user_email: str = Field(..., description="Email of the user")
    user_name: str = Field(..., description="Full name of the user")
    address: str = Field(..., description="User's physical address")
    id_front_image: str = Field(..., description="Base64 encoded image of ID front")
    id_back_image: str = Field(..., description="Base64 encoded image of ID back")
    about_user_article_link: HttpUrl = Field(..., description="Link to an article about the user")
    status: VerificationStatus = Field(default=VerificationStatus.PENDING,
                                       description="Current status of the verification request")
    request_date: datetime = Field(default_factory=datetime.utcnow, description="Date when request was submitted")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }


# Response model - what users see when getting verification requests
class VerificationRequestResponse(BaseModel):
    id: str = Field(..., description="Verification request ID")
    user_id: str = Field(..., description="ID of the user who submitted the request")
    user_email: str = Field(..., description="Email of the user")
    user_name: str = Field(..., description="Full name of the user")
    address: str = Field(..., description="User's physical address")
    id_front_image: str = Field(..., description="Base64 encoded image of ID front")
    id_back_image: str = Field(..., description="Base64 encoded image of ID back")
    about_user_article_link: HttpUrl = Field(..., description="Link to an article about the user")
    status: VerificationStatus = Field(..., description="Current status of the verification request")
    request_date: str = Field(..., description="Formatted date when request was submitted")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "68298f838b7e3d09bb3babcb",
                "user_id": "6809644fd457793bad901156",
                "user_email": "john.doe@example.com",
                "user_name": "John Doe",
                "address": "123 Main St, City, Country",
                "id_front_image": "base64_encoded_string...",
                "id_back_image": "base64_encoded_string...",
                "about_user_article_link": "https://example.com/about-user",
                "status": "pending",
                "request_date": "2025-05-18 07:57:10"
            }
        }