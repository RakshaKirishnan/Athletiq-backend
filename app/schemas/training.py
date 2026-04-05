from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum


class IntensityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TrainingSessionBase(BaseModel):
    workout_name: str
    intensity_level: IntensityLevel
    duration_minutes: float
    calories_burned: Optional[float] = None
    coach_remarks: Optional[str] = None
    completed_at: datetime


class TrainingSessionCreate(TrainingSessionBase):
    athlete_id: UUID


class TrainingSessionUpdate(BaseModel):
    workout_name: Optional[str] = None
    intensity_level: Optional[IntensityLevel] = None
    duration_minutes: Optional[float] = None
    calories_burned: Optional[float] = None
    coach_remarks: Optional[str] = None
    completed_at: Optional[datetime] = None


class TrainingSessionResponse(TrainingSessionBase):
    id: UUID
    athlete_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
