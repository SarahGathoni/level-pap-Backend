from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class TrainerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    bio: Optional[str] = None
    photo: Optional[str] = None
    specializations: Optional[List[str]] = None
    years_of_experience: Optional[int] = None
    certifications: Optional[List[str]] = None


class TrainerCreate(TrainerBase):
    user_id: Optional[UUID] = None


class TrainerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    bio: Optional[str] = None
    photo: Optional[str] = None
    specializations: Optional[List[str]] = None
    years_of_experience: Optional[int] = None
    certifications: Optional[List[str]] = None
    is_active: Optional[bool] = None


class TrainerResponse(TrainerBase):
    id: UUID
    user_id: Optional[UUID] = None
    rating: Optional[Decimal] = None
    total_courses_taught: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

