from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class MetricSummary(BaseModel):
    metric_type: str
    latest_value: float
    average_value: Optional[float]
    unit: str
    recorded_at: datetime


class TrendPoint(BaseModel):
    timestamp: datetime
    value: float
    metric_type: str


class AthleteSummary(BaseModel):
    athlete_id: str
    name: str
    latest_speed: Optional[float]
    latest_stamina: Optional[float]
    latest_strength: Optional[float]
    latest_heart_rate: Optional[float]
    latest_vo2_max: Optional[float]
    latest_sleep: Optional[float]
    latest_recovery: Optional[float]
    latest_fatigue: Optional[float]
    total_training_sessions: int
    total_training_minutes: float


class MetricComparison(BaseModel):
    metric_type: str
    athlete_comparisons: List[Dict]


class HeatmapData(BaseModel):
    date: str
    intensity_level: str
    count: int


class GlobalSummary(BaseModel):
    total_athletes: int
    total_training_sessions: int
    sessions_today: int
    sessions_this_week: int
    most_active_athlete: Optional[str]  # athlete name


class AthleteTeamSummary(BaseModel):
    athlete_id: str
    name: str
    latest_speed: Optional[float]
    latest_stamina: Optional[float]
    latest_strength: Optional[float]
    latest_heart_rate: Optional[float]
    latest_vo2_max: Optional[float]
    latest_sleep: Optional[float]
    latest_recovery: Optional[float]
    latest_fatigue: Optional[float]
    total_training_sessions: int
