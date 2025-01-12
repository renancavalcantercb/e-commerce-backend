from app.core.database import users_collection
from app.schemas.user import UserCreate
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ as env

async def is_email_or_cpf_taken(email: str, cpf: str) -> bool:
    user = await users_collection.find_one({"$or": [{"email": email}, {"cpf": cpf}]})
    return user is not None


async def create_user(user_data: UserCreate) -> dict:
    if await is_email_or_cpf_taken(user_data.email, user_data.cpf):
        raise ValueError("Email or CPF already exists.")

    user = {
        "name": user_data.name,
        "email": user_data.email,
        "password": generate_password_hash(user_data.password),
        "cpf": user_data.cpf,
        "created_at": datetime.utcnow(),
        "confirmed": False,
    }
    result = await users_collection.insert_one(user)
    return {"id": str(result.inserted_id), "token": user["token"]}


async def login_user(email: str, password: str) -> dict:
    user = await users_collection.find_one({"email": email})
    
    if not user or not check_password_hash(user["password"], password):
        raise ValueError("Invalid email or password.")
    
    token = jwt.encode(
            {
                "user_id": str(user["_id"]),
                "name": user["name"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            },
            key=env.get("SECRET_KEY"),
            algorithm="HS256",
        )
    
    return {"token": token}