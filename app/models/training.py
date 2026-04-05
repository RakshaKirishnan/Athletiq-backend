from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Uuid, Enum as SQLEnum
from datetime import datetime
from uuid import uuid4
from enum import Enum
from app.db.base import Base


class IntensityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(Uuid, primary_key=True, default=uuid4)
    athlete_id = Column(Uuid, ForeignKey("athletes.id"), nullable=False)
    workout_name = Column(String(255), nullable=False)
    intensity_level = Column(SQLEnum(IntensityLevel), nullable=False)
    duration_minutes = Column(Float, nullable=False)
    calories_burned = Column(Float, nullable=True)
    coach_remarks = Column(String, nullable=True)
    completed_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
