from datetime import date, datetime, timezone
from pydantic import BaseModel, EmailStr, Field
import re


# User model for database
class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    contact: str
    birthday: date
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "StrongPassword123!",
                "contact": "+1234567890",
                "birthday": "1990-01-01"
            }
        }


# Schema for user sign-up
class UserSignUp(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    contact: str
    birthday: date

    @classmethod
    def strong_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

    @classmethod
    def validate_contact(cls, v):
        if not re.match(r'^\+?[0-9]{10,15}$', v):
            raise ValueError('Contact must be a valid phone number (10-15 digits with optional + prefix)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "StrongPassword123!",
                "contact": "+1234567890",
                "birthday": "1990-01-01"
            }
        }


# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "StrongPassword123!"
            }
        }


# Schema for token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Schema for user response (excluding sensitive information)
class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    contact: str
    birthday: date
    created_at: datetime
    updated_at: datetime