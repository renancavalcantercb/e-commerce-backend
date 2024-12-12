from flask import Blueprint, request
from application import db
from application.utils.responses import create_response

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        size = int(request.args.get("size", 10))
        page = int(request.args.get("page", 1))
        offset = (page - 1) * size

        products = db.products.find().skip(offset).limit(size)
        return create_response(
            "Products retrieved successfully", 200, data=list(products)
        )

    elif request.method == "POST":
        data = request.get_json()
        try:
            db.products.insert_one(data)
            return create_response("Product successfully created!", 201)
        except Exception as e:
            return create_response(f"Error creating product: {str(e)}", 500)
