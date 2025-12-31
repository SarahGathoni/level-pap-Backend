from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from app.core.enums import CourseCategory, Audience


class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    category: CourseCategory
    audience: Audience
    description: str = Field(..., min_length=1)
    duration_weeks: Optional[int] = None
    price: Optional[Decimal] = None
    syllabus: List[str] = Field(..., min_items=1)
    image: Optional[str] = None


class CourseCreate(CourseBase):
    trainer_id: Optional[UUID] = None


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[CourseCategory] = None
    audience: Optional[Audience] = None
    description: Optional[str] = None
    duration_weeks: Optional[int] = None
    price: Optional[Decimal] = None
    syllabus: Optional[List[str]] = None
    image: Optional[str] = None
    trainer_id: Optional[UUID] = None
    is_published: Optional[bool] = None
    is_active: Optional[bool] = None


class CourseResponse(CourseBase):
    id: UUID
    trainer_id: Optional[UUID] = None
    is_published: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

