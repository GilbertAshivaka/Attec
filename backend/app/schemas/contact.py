from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.contact import ContactStatus


# Request schemas
class ContactSubmissionCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    company: Optional[str] = Field(None, max_length=100)
    message: str = Field(..., min_length=10, max_length=2000)


class ContactSubmissionUpdate(BaseModel):
    status: Optional[ContactStatus] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


# Response schemas
class ContactSubmissionResponse(BaseModel):
    id: UUID
    name: str
    email: str
    company: Optional[str]
    message: str
    status: ContactStatus
    ip_address: Optional[str]
    assigned_to: Optional[str]
    notes: Optional[str]
    submitted_at: datetime
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class ContactSubmissionList(BaseModel):
    total: int
    items: list[ContactSubmissionResponse]
    skip: int
    limit: int
