from flask import Blueprint
from application.routes.products import products_bp
from application.routes.auth import auth_bp
from application.routes.profile import profile_bp


def register_blueprints(app):
    app.register_blueprint(products_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(profile_bp, url_prefix="/api")
