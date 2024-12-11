from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from os import environ

import sys
import os

sys.path.append(os.getcwd())

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
app.config["MONGO_URI"] = environ.get("MONGO_URI")
app.config["MAIL_SERVER"] = environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = environ.get("MAIL_PORT")
app.config["MAIL_USERNAME"] = environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = environ.get("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

client = MongoClient(app.config["MONGO_URI"], connect=False)
db = client["e-commerce"]
products = db["products"]

CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST", "GET", "OPTIONS"]}})


from application.routes import *
