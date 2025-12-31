from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from app.core.enums import PaymentProvider, PaymentTransactionStatus


class PaymentInitiate(BaseModel):
    booking_id: UUID
    provider: PaymentProvider
    phone: Optional[str] = None  # For M-Pesa
    email: Optional[EmailStr] = None  # For Flutterwave


class PaymentCreate(BaseModel):
    booking_id: UUID
    provider: PaymentProvider
    payment_reference: str
    amount: Decimal
    currency: str = "KES"


class PaymentResponse(BaseModel):
    id: UUID
    booking_id: UUID
    provider: PaymentProvider
    payment_reference: str
    amount: Decimal
    currency: str
    status: PaymentTransactionStatus
    provider_transaction_id: Optional[str] = None
    initiated_at: datetime
    completed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

