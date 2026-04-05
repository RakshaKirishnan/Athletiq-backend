"""Comparison service — async SQLAlchemy."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List, Dict

from app.models.metrics import (
    SpeedMetric, StaminaMetric, StrengthMetric, HeartRateMetric,
    VO2MaxMetric, SleepMetric, RecoveryMetric, FatigueMetric,
)
from app.models.athlete import Athlete

_METRIC_MODELS = {
    "speed": SpeedMetric,
    "stamina": StaminaMetric,
    "strength": StrengthMetric,
    "heart_rate": HeartRateMetric,
    "heart-rate": HeartRateMetric,   # accept both forms from frontend/URL
    "vo2_max": VO2MaxMetric,
    "vo2-max": VO2MaxMetric,         # accept both forms from frontend/URL
    "sleep": SleepMetric,
    "recovery": RecoveryMetric,
    "fatigue": FatigueMetric,
}


class ComparisonService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_metric_comparison(
        self, athlete_ids: List[UUID], metric_type: str
    ) -> List[Dict]:
        model = _METRIC_MODELS.get(metric_type)
        if not model:
            return []

        results = []
        for athlete_id in athlete_ids:
            athlete_result = await self.db.execute(
                select(Athlete).filter(Athlete.id == athlete_id)
            )
            athlete = athlete_result.scalars().first()
            if not athlete:
                continue

            metric_result = await self.db.execute(
                select(model)
                .filter(model.athlete_id == athlete_id)
                .order_by(model.recorded_at.desc())
                .limit(1)
            )
            metric = metric_result.scalars().first()
            if metric:
                results.append({
                    "athlete_id": str(athlete_id),
                    "athlete_name": athlete.name,
                    "metric_type": metric_type,
                    "value": metric.value,
                    "unit": metric.unit,
                })
        return results

    async def get_radar_comparison(self, athlete_ids: List[UUID]) -> List[Dict]:
        results = []
        for athlete_id in athlete_ids:
            athlete_result = await self.db.execute(
                select(Athlete).filter(Athlete.id == athlete_id)
            )
            athlete = athlete_result.scalars().first()
            if not athlete:
                continue

            metrics: Dict[str, float] = {}
            for metric_type, model in _METRIC_MODELS.items():
                m_result = await self.db.execute(
                    select(model)
                    .filter(model.athlete_id == athlete_id)
                    .order_by(model.recorded_at.desc())
                    .limit(1)
                )
                metric = m_result.scalars().first()
                metrics[metric_type] = metric.value if metric else 0

            results.append({
                "athlete_id": str(athlete_id),
                "athlete_name": athlete.name,
                "metrics": metrics,
            })
        return results
