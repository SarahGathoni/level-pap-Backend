from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date, time
from uuid import UUID
from app.core.enums import SessionStatus


class SessionBase(BaseModel):
    course_id: UUID
    date: date
    start_time: time
    end_time: Optional[time] = None
    location: str = Field(..., min_length=1)
    trainer_id: Optional[UUID] = None
    capacity: int = Field(1, ge=1)
    notes: Optional[str] = None


class SessionCreate(SessionBase):
    @validator('date')
    def validate_future_date(cls, v):
        if v < date.today():
            raise ValueError('Session date must be in the future')
        return v


class SessionUpdate(BaseModel):
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = None
    trainer_id: Optional[UUID] = None
    capacity: Optional[int] = Field(None, ge=1)
    status: Optional[SessionStatus] = None
    notes: Optional[str] = None


class SessionResponse(SessionBase):
    id: UUID
    seats_booked: int
    status: SessionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

