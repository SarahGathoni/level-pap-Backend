from sqlalchemy import Column, String, Integer, Boolean, DateTime, Date, Time, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base
from app.core.enums import SessionStatus


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=True)
    location = Column(String, nullable=False)
    trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.id"), nullable=True, index=True)
    capacity = Column(Integer, default=1, nullable=False)
    seats_booked = Column(Integer, default=0, nullable=False)
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.SCHEDULED, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    course = relationship("Course", back_populates="sessions")
    trainer = relationship("Trainer", foreign_keys=[trainer_id])
    bookings = relationship("Booking", back_populates="session")

