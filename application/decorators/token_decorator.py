import jwt
from functools import wraps
from flask import request, jsonify
from application import app, db


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!", "status": 401}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user_id = data["user_id"]
        except Exception as e:
            return jsonify({"message": "Invalid token", "status": 401}), 401
        return f(*args, **kwargs)

    return decorated
