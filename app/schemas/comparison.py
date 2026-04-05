from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID


class AthleteMetricComparison(BaseModel):
    athlete_id: UUID
    athlete_name: str
    metric_type: str
    value: float
    unit: str


class RadarComparisonData(BaseModel):
    athlete_id: UUID
    athlete_name: str
    metrics: Dict[str, float]


class ComparisonStats(BaseModel):
    metric_type: str
    athletes: List[Dict]
