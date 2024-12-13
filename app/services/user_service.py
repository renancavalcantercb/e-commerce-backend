from app.core.database import users_collection
from app.schemas.user import UserCreate
from datetime import datetime
from bson import ObjectId
from hashlib import sha256

async def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()

async def is_email_or_cpf_taken(email: str, cpf: str) -> bool:
    user = await users_collection.find_one({"$or": [{"email": email}, {"cpf": cpf}]})
    return user is not None

async def create_user(user_data: UserCreate) -> dict:
    if await is_email_or_cpf_taken(user_data.email, user_data.cpf):
        raise ValueError("Email or CPF already exists.")

    user = {
        "name": user_data.name,
        "email": user_data.email,
        "password": await hash_password(user_data.password),
        "cpf": user_data.cpf,
        "token": str(ObjectId()),
        "created_at": datetime.utcnow(),
        "confirmed": False,
    }
    result = await users_collection.insert_one(user)
    return {"id": str(result.inserted_id), "token": user["token"]}
