from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Numeric, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base
from app.core.enums import PaymentStatus


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False, index=True)
    seats = Column(Integer, default=1, nullable=False)
    payment_status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    contact_phone = Column(String, nullable=True)
    special_requirements = Column(Text, nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="bookings")
    session = relationship("Session", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'session_id', name='unique_user_session_booking'),
    )

