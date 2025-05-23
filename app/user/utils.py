from datetime import datetime
from bson import ObjectId


def user_helper(user) -> dict:
    """
    Convert MongoDB user document to a dict with properly formatted fields
    """
    user_id = str(user["_id"]) if "_id" in user else user.get("id")

    return {
        "id": user_id,
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "contact": user["contact"],
        "birthday": user["birthday"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def parse_user_from_db(user_data):
    """
    Parse user data from database to proper format
    """
    if not user_data:
        return None

    user_data["id"] = str(user_data["_id"])
    del user_data["_id"]

    if "password" in user_data:
        del user_data["password"]

    return user_data


def verification_request_helper(request) -> dict:
    """
    Format verification request data
    """
    return {
        "verification_id": str(request["_id"]),
        "user_id": request["user_id"],
        "address": request["address"],
        "id_front_image": request["id_front_image"],
        "id_back_image": request["id_back_image"],
        "about_user_article_link": request["about_user_article_link"],
        "status": request["status"],
        "request_date": request["request_date"].strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(request["request_date"], datetime.datetime)
            else request["request_date"],
    }



def user_details_helper(user) -> dict:
    """
    Format user details for response
    """
    return {
        "id": str(user["id"]),
        "first_name": user.get("first_name", ""),
        "last_name": user.get("last_name", ""),
        "email": user.get("email", ""),
        "contact": user.get("contact", ""),
        "birthday": user.get("birthday", ""),
        "profile_image": user.get("profile_image", ""),
        "cover_image": user.get("cover_image", ""),
        "user_type": user.get("user_type", ""),
        "bio": user.get("bio", ""),
        "facebook": user.get("facebook", ""),
        "instagram": user.get("instagram", ""),
        "twitter": user.get("twitter", ""),
        "linkedin": user.get("linkedin", ""),
        "verification_status": user.get("verification_status", ""),
        "created_at": user.get("created_at", ""),
        "updated_at": user.get("updated_at", "")
    }