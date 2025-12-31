from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Numeric, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base
from app.core.enums import PaymentProvider, PaymentTransactionStatus


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), unique=True, nullable=False, index=True)
    provider = Column(SQLEnum(PaymentProvider), nullable=False)
    payment_reference = Column(String, unique=True, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="KES", nullable=False)
    status = Column(SQLEnum(PaymentTransactionStatus), default=PaymentTransactionStatus.PENDING, nullable=False, index=True)
    provider_response = Column(JSON, nullable=True)
    provider_transaction_id = Column(String, nullable=True, index=True)
    initiated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    failure_reason = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    booking = relationship("Booking", back_populates="payment")
    webhooks = relationship("PaymentWebhook", back_populates="payment")


class PaymentWebhook(Base):
    __tablename__ = "payment_webhooks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), nullable=True, index=True)
    provider = Column(SQLEnum(PaymentProvider), nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    processed = Column(Boolean, default=False, nullable=False, index=True)
    processing_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    payment = relationship("Payment", back_populates="webhooks")

