from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from app.core.enums import PaymentStatus


class BookingBase(BaseModel):
    session_id: UUID
    seats: int = Field(1, ge=1)
    contact_phone: Optional[str] = None
    special_requirements: Optional[str] = None


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    seats: Optional[int] = Field(None, ge=1)
    contact_phone: Optional[str] = None
    special_requirements: Optional[str] = None
    cancellation_reason: Optional[str] = None


class BookingResponse(BookingBase):
    id: UUID
    user_id: UUID
    payment_status: PaymentStatus
    total_amount: Decimal
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

