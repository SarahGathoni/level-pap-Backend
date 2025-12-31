from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Numeric, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base
from app.core.enums import CorporateRequestStatus


class CorporateRequest(Base):
    __tablename__ = "corporate_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String, nullable=False, index=True)
    contact_person = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    preferred_dates = Column(ARRAY(String), nullable=True)
    preferred_time = Column(String, nullable=True)
    location = Column(String, nullable=True)
    headcount = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(SQLEnum(CorporateRequestStatus), default=CorporateRequestStatus.PENDING, nullable=False, index=True)
    assigned_to_trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.id"), nullable=True, index=True)
    quoted_price = Column(Numeric(10, 2), nullable=True)
    admin_notes = Column(Text, nullable=True)
    responded_at = Column(DateTime(timezone=True), nullable=True)
    responded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    trainer = relationship("Trainer", foreign_keys=[assigned_to_trainer_id])
    admin_user = relationship("User", foreign_keys=[responded_by])

