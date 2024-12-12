from flask import Blueprint, request
from application import db
from application.decorators.token_decorator import token_required
from application.utils.responses import create_response

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET"])
@token_required
def profile():
    user_id = request.user_id
    user = db.users.find_one({"_id": user_id})
    if not user:
        return create_response("User not found", 404)

    return create_response(
        "User found", 200, {"name": user["name"], "email": user["email"]}
    )
