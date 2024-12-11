import datetime
import jwt
from application import app, db
from bson import json_util
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from application.decorators.token_decorator import token_required
from application.utils.utils import (
    clean_cpf,
    generate_confirmation_token,
    send_confirmation_email,
)


@app.route("/api")
def index():
    return jsonify({"message": "Welcome to the API!", "status": 200}), 200


@app.route("/api/products", methods=["GET", "POST"])
def products(size: int = 10, page: int = 1):
    if request.method == "GET":
        size = int(request.args.get("size", 10))
        page = int(request.args.get("page", 1))

        offset = (page - 1) * size

        products = db.products.find().skip(offset).limit(size)
        return json_util.dumps(products)

    elif request.method == "POST":
        data = request.get_json()

        title = data.get("name")
        price = data.get("price")
        sale_price = data.get("sale_price")
        on_sale = data.get("on_sale")
        description = data.get("description")
        image = data.get("image")
        category = data.get("category")
        quantity = data.get("quantity")
        rating = data.get("rating")
        reviews = data.get("reviews")

        try:
            db.products.insert_one(
                {
                    "title": title,
                    "price": price,
                    "sale_price": sale_price,
                    "on_sale": on_sale,
                    "description": description,
                    "image": image,
                    "category": category,
                    "quantity": quantity,
                    "rating": rating,
                    "reviews": reviews,
                }
            )
            return (
                jsonify({"message": "Product successfully created!", "status": 201}),
                201,
            )
        except Exception as e:
            return (
                jsonify(
                    {"message": "Error creating product: " + str(e), "status": 500}
                ),
                500,
            )

    return jsonify({"message": "Invalid request method", "status": 400}), 400


@app.route("/api/register", methods=["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        cpf = data.get("cpf")
        birth_date = data.get("birth_date")
        phone = data.get("phone")
        admin = data.get("admin", False)

        if (
            not name
            or not email
            or not password
            or not cpf
            or not birth_date
            or not phone
        ):
            return jsonify({"message": "Missing fields", "status": 400}), 400

        existing_user = db.users.find_one({"$or": [{"email": email}, {"cpf": cpf}]})
        if existing_user:
            return (
                jsonify({"message": "Email or CPF already exists", "status": 400}),
                400,
            )

        token = generate_confirmation_token()

        try:
            db.users.insert_one(
                {
                    "name": name,
                    "email": email,
                    "password": generate_password_hash(password),
                    "cpf": clean_cpf(cpf),
                    "birth_date": birth_date,
                    "phone": phone,
                    "admin": admin,
                    "confirmed": False,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                    "token": token,
                    "created_at": datetime.datetime.utcnow(),
                }
            )
            send_confirmation_email(email, token)
            return (
                jsonify({"message": "User successfully created!", "status": 201}),
                201,
            )
        except Exception as e:
            return (
                jsonify({"message": "Error creating user: " + str(e), "status": 500}),
                500,
            )

    return jsonify({"error": "Invalid request method", "status": 400}), 400


@app.route("/api/confirm/<token>", methods=["GET"])
def confirm_email(token):
    try:
        user = db.users.find_one({"token": token})
        if user:
            if datetime.datetime.utcnow() > user["exp"]:
                return jsonify({"message": "Token expired", "status": 400}), 400
            else:
                db.users.update_one({"_id": user["_id"]}, {"$set": {"confirmed": True}})
                return (
                    jsonify({"message": "User successfully confirmed!", "status": 200}),
                    200,
                )
    except Exception as e:
        return jsonify({"message": "Error finding user: " + str(e), "status": 500}), 500


@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Missing fields", "status": 400}), 400

        user = db.users.find_one({"email": email})
        if not user or not check_password_hash(user["password"], password):
            return jsonify({"message": "Invalid credentials", "status": 400}), 400

        token = jwt.encode(
            {
                "user_id": str(user["_id"]),
                "name": user["name"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        return (
            jsonify(
                {
                    "message": "User successfully logged in!",
                    "token": token,
                    "status": 200,
                }
            ),
            200,
        )

    return jsonify({"message": "Invalid request method", "status": 400}), 400


@app.route("/api/profile", methods=["GET"])
@token_required
def profile():
    user_id = request.user_id

    user = db.users.find_one({"_id": user_id})
    if not user:
        return jsonify({"message": "User not found", "status": 404}), 404

    return (
        jsonify(
            {
                "message": "User found",
                "name": user["name"],
                "email": user["email"],
                "cpf": user["cpf"],
                "birth_date": user["birth_date"],
                "phone": user["phone"],
                "status": 200,
            }
        ),
        200,
    )


@app.route("/api/profile/edit", methods=["POST"])
@token_required
def update_profile():
    user_id = request.user_id
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    if not name or not email or not phone:
        return jsonify({"message": "Missing fields", "status": 400}), 400

    try:
        db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "name": name,
                    "email": email,
                    "phone": phone,
                }
            },
        )
        return (
            jsonify({"message": "User successfully updated!", "status": 200}),
            200,
        )
    except Exception as e:
        return (
            jsonify({"message": "Error updating user: " + str(e), "status": 500}),
            500,
        )

    return jsonify({"message": "Invalid request method", "status": 400}), 400
