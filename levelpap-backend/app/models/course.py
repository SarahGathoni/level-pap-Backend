from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Numeric, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base
from app.core.enums import CourseCategory, Audience


class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    category = Column(SQLEnum(CourseCategory), nullable=False, index=True)
    audience = Column(SQLEnum(Audience), nullable=False, index=True)
    description = Column(Text, nullable=False)
    duration_weeks = Column(Integer, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    syllabus = Column(ARRAY(String), nullable=False)
    image = Column(String, nullable=True)
    trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.id"), nullable=True, index=True)
    is_published = Column(Boolean, default=False, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    trainer = relationship("Trainer", back_populates="courses")
    sessions = relationship("Session", back_populates="course")

