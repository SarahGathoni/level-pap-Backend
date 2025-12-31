from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Numeric, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=True)
    name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    photo = Column(String, nullable=True)
    specializations = Column(ARRAY(String), nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    certifications = Column(ARRAY(String), nullable=True)
    rating = Column(Numeric(3, 2), nullable=True)
    total_courses_taught = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="trainer_profile", uselist=False)
    courses = relationship("Course", back_populates="trainer")

