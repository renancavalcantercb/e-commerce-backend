from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
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
