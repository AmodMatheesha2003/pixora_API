from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import os
from bson import ObjectId

from app.auth.models import UserSignUp, UserLogin, TokenResponse
from app.auth.password_handler import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.database import get_db

auth_router = APIRouter()


@auth_router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserSignUp = Body(...)):
    db = await get_db()

    # Check if user with email already exists
    user_exists = await db["users"].find_one({"email": user_data.email})
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create user dict with hashed password
    new_user = {
        "_id": str(ObjectId()),
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "email": user_data.email,
        "password": hashed_password,
        "contact": user_data.contact,
        "birthday": user_data.birthday.strftime("%Y-%m-%d"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    # Insert user into database
    await db["users"].insert_one(new_user)

    return {
        "message": "User created successfully",
        "id": new_user["_id"]
    }


@auth_router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = await get_db()

    # Find user by email
    user = await db["users"].find_one({"email": form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": user["_id"]},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}