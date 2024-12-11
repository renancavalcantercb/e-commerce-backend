import re
import uuid
from flask import url_for
from flask_mail import Message, Mail
from application import app
from dotenv import load_dotenv
from os import environ

load_dotenv()


def clean_cpf(cpf: str) -> str:
    """Clean CPF string removing all non-numeric characters."""
    return re.sub(r"[^0-9]", "", cpf)


def generate_confirmation_token():
    """
    Generate a token for confirm user email.
    """
    token = str(uuid.uuid4())
    return token


def send_confirmation_email(email, token):
    """
    Send a confirmation email to the user.
    """
    mail = Mail(app)

    msg = Message(
        "Confirm your email",
        sender=environ.get("MAIL_USERNAME"),
        recipients=[email],
    )
    print(token)
    confirmation_link = url_for("confirm_email", token=token, _external=True)
    msg.body = f"Your confirmation link is {confirmation_link}"

    mail.send(msg)
