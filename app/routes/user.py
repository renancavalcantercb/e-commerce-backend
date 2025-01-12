from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse, LoginResponse
from app.services.user_service import create_user, login_user
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def register_user(user: UserCreate):
    try:
        new_user = await create_user(user)
        return {
            "name": user.name,
            "email": user.email,
            "cpf": user.cpf,
            "token": new_user["token"],
            "created_at": datetime.utcnow(),
            "confirmed": False,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login(email: str, password: str):
    try:
        user = await login_user(email, password)
        return {"token": user["token"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))