from datetime import datetime
from bson import ObjectId


def format_verification_request(request):
    """
    Format verification request data for response
    """
    return {
        "id": str(request["_id"]),
        "user_id": request["user_id"],
        "user_email": request["user_email"],
        "user_name": request["user_name"],
        "address": request["address"],
        "id_front_image": request["id_front_image"],
        "id_back_image": request["id_back_image"],
        "about_user_article_link": request["about_user_article_link"],
        "status": request["status"],
        "request_date": request["request_date"].strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(request["request_date"], datetime)
        else request["request_date"],
        "profile_image": request["profile_image"],
    }