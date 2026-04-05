from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class MetricBase(BaseModel):
    value: float
    unit: str
    notes: Optional[str] = None


class SpeedMetricCreate(MetricBase):
    athlete_id: UUID


class SpeedMetricResponse(MetricBase):
    id: UUID
    athlete_id: UUID
    recorded_at: datetime

    class Config:
        from_attributes = True


class StaminaMetricCreate(MetricBase):
    athlete_id: UUID


class StaminaMetricResponse(MetricBase):
    id: UUID
    athlete_id: UUID
    recorded_at: datetime

    class Config:
        from_attributes = True


class StrengthMetricCreate(MetricBase):
    athlete_id: UUID


class StrengthMetricResponse(MetricBase):
    id: UUID
    athlete_id: UUID
    recorded_at: datetime

    class Config:
        from_attributes = True


class HeartRateMetricCreate(MetricBase):
    athlete_id: UUID


class HeartRateMetricResponse(MetricBase):
    id: UUID
    athlete_id: UUID
    recorded_at: datetime

    class Config:
        from_attributes = True


class VO2MaxMetricCreate(MetricBase):
    athlete_id: UUID


class VO2MaxMetricResponse(MetricBase):
    id: UUID
    athlete_id: UUID
    recorded_at: datetime

    class Config:
        from_attributes = True


class SleepMetricCreate(MetricBase):
    athlete_id: UUID


class SleepMetricResponse(MetricBase):
    id: UUID
    athlete_id: UUID
    recorded_at: datetime

    class Config:
        from_attributes = True


class RecoveryMetricCreate(MetricBase):
    athlete_id: UUID


class RecoveryMetricResponse(MetricBase):
    id: UUID
    athlete_id: UUID
    recorded_at: datetime

    class Config:
        from_attributes = True


class FatigueMetricCreate(MetricBase):
    athlete_id: UUID


class FatigueMetricResponse(MetricBase):
    id: UUID
    athlete_id: UUID
    recorded_at: datetime

    class Config:
        from_attributes = True
