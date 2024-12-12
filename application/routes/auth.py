import datetime
import jwt
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from application import db, app
from application.utils.responses import create_response
from application.utils.utils import generate_confirmation_token, send_confirmation_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name, email, password, cpf = (
        data.get("name"),
        data.get("email"),
        data.get("password"),
        data.get("cpf"),
    )
    if not all([name, email, password, cpf]):
        return create_response("Missing fields", 400)

    if db.users.find_one({"$or": [{"email": email}, {"cpf": cpf}]}):
        return create_response("Email or CPF already exists", 400)

    try:
        db.users.insert_one(
            {
                "name": name,
                "email": email,
                "password": generate_password_hash(password),
                "cpf": cpf,
                "token": generate_confirmation_token(),
                "created_at": datetime.datetime.utcnow(),
                "confirmed": False,
            }
        )
        send_confirmation_email(email)
        return create_response("User successfully created!", 201)
    except Exception as e:
        return create_response(f"Error creating user: {str(e)}", 500)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")
    user = db.users.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return create_response("Invalid credentials", 400)

    token = jwt.encode(
        {
            "user_id": str(user["_id"]),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return create_response("Login successful", 200, {"token": token})
