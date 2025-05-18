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


class VerificationRequest(BaseModel):
    address: str
    id_front_image: str
    id_back_image: str
    about_user_article_link: str

    class Config:
        json_schema_extra = {
            "example": {
                "address": "123 Main St, City, Country",
                "id_front_image": "base64_encoded_string...",
                "id_back_image": "base64_encoded_string...",
                "about_user_article_link": "https://example.com/about-user"
            }
        }