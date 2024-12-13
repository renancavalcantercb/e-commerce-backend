from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    cpf: str

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    token: str
    created_at: datetime
    confirmed: bool
