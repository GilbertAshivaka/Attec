from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import UserRole


# Request schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: UserRole = UserRole.VIEWER


# Response schemas
class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    role: UserRole
    active: bool
    last_login: Optional[datetime]
    created_at: datetime
    
    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
