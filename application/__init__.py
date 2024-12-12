import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv

if os.getenv("FLASK_ENV") != "production":
    load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurações da aplicação
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

# Inicializando MongoDB
client = MongoClient(app.config["MONGO_URI"], connect=False)
db = client["e-commerce"]

# Registro dos blueprints
from application.routes import register_blueprints

register_blueprints(app)
