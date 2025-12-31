from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from app.core.enums import CorporateRequestStatus


class CorporateRequestBase(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=200)
    contact_person: str = Field(..., min_length=1)
    email: EmailStr
    phone: str
    topic: str = Field(..., min_length=2, max_length=500)
    preferred_dates: Optional[List[str]] = None
    preferred_time: Optional[str] = None
    location: Optional[str] = None
    headcount: Optional[int] = None
    notes: Optional[str] = None


class CorporateRequestCreate(CorporateRequestBase):
    @validator('preferred_dates', pre=True)
    def validate_dates(cls, v):
        if v:
            # Validate ISO date strings
            from datetime import datetime
            for date_str in v:
                try:
                    datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError(f'Invalid date format: {date_str}')
        return v


class CorporateRequestUpdate(BaseModel):
    status: Optional[CorporateRequestStatus] = None
    assigned_to_trainer_id: Optional[UUID] = None
    quoted_price: Optional[Decimal] = None
    admin_notes: Optional[str] = None


class CorporateRequestResponse(CorporateRequestBase):
    id: UUID
    status: CorporateRequestStatus
    assigned_to_trainer_id: Optional[UUID] = None
    quoted_price: Optional[Decimal] = None
    admin_notes: Optional[str] = None
    responded_at: Optional[datetime] = None
    responded_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

