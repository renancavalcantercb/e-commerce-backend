from functools import wraps
from flask import request, jsonify
from application import app
from bson import ObjectId
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or "Bearer " not in auth_header:
            return jsonify({"message": "Missing token", "status": 400}), 400

        token = auth_header.split(" ")[1]

        try:
            decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user_id = ObjectId(decoded["user_id"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Expired token", "status": 400}), 400
        except Exception as e:
            print(e)
            return jsonify({"message": "Invalid token", "status": 400}), 400

        return f(*args, **kwargs)

    return decorated
