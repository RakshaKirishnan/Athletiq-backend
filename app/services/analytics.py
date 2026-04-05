"""Analytics service — async SQLAlchemy."""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from app.models.metrics import (
    SpeedMetric, StaminaMetric, StrengthMetric, HeartRateMetric,
    VO2MaxMetric, SleepMetric, RecoveryMetric, FatigueMetric,
)
from app.models.training import TrainingSession
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


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _latest(self, model, athlete_id: UUID):
        result = await self.db.execute(
            select(model)
            .filter(model.athlete_id == athlete_id)
            .order_by(model.recorded_at.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def get_athlete_summary(self, athlete_id: UUID) -> Optional[Dict]:
        result = await self.db.execute(
            select(Athlete).filter(Athlete.id == athlete_id)
        )
        athlete = result.scalars().first()
        if not athlete:
            return None

        latest_speed = await self._latest(SpeedMetric, athlete_id)
        latest_stamina = await self._latest(StaminaMetric, athlete_id)
        latest_strength = await self._latest(StrengthMetric, athlete_id)
        latest_heart_rate = await self._latest(HeartRateMetric, athlete_id)
        latest_vo2_max = await self._latest(VO2MaxMetric, athlete_id)
        latest_sleep = await self._latest(SleepMetric, athlete_id)
        latest_recovery = await self._latest(RecoveryMetric, athlete_id)
        latest_fatigue = await self._latest(FatigueMetric, athlete_id)

        sessions_result = await self.db.execute(
            select(TrainingSession).filter(TrainingSession.athlete_id == athlete_id)
        )
        training_sessions = list(sessions_result.scalars().all())

        return {
            "athlete_id": str(athlete_id),
            "name": athlete.name,
            "latest_speed": latest_speed.value if latest_speed else None,
            "latest_stamina": latest_stamina.value if latest_stamina else None,
            "latest_strength": latest_strength.value if latest_strength else None,
            "latest_heart_rate": latest_heart_rate.value if latest_heart_rate else None,
            "latest_vo2_max": latest_vo2_max.value if latest_vo2_max else None,
            "latest_sleep": latest_sleep.value if latest_sleep else None,
            "latest_recovery": latest_recovery.value if latest_recovery else None,
            "latest_fatigue": latest_fatigue.value if latest_fatigue else None,
            "total_training_sessions": len(training_sessions),
            "total_training_minutes": sum(s.duration_minutes for s in training_sessions),
        }

    async def get_metric_trends(
        self, athlete_id: UUID, metric_type: str, days: int = 30
    ) -> List[Dict]:
        model = _METRIC_MODELS.get(metric_type)
        if not model:
            return []

        start_date = datetime.utcnow() - timedelta(days=days)
        result = await self.db.execute(
            select(model).filter(
                model.athlete_id == athlete_id,
                model.recorded_at >= start_date,
            ).order_by(model.recorded_at.asc())
        )
        return [
            {"timestamp": m.recorded_at, "value": m.value, "metric_type": metric_type}
            for m in result.scalars().all()
        ]

    async def get_training_heatmap(self, athlete_id: UUID, days: int = 30) -> List[Dict]:
        start_date = datetime.utcnow() - timedelta(days=days)
        result = await self.db.execute(
            select(TrainingSession).filter(
                TrainingSession.athlete_id == athlete_id,
                TrainingSession.completed_at >= start_date,
            )
        )
        heatmap: Dict[str, Dict] = {}
        for session in result.scalars().all():
            date_str = session.completed_at.strftime("%Y-%m-%d")
            intensity = session.intensity_level.value
            key = f"{date_str}_{intensity}"
            if key not in heatmap:
                heatmap[key] = {"date": date_str, "intensity_level": intensity, "count": 0}
            heatmap[key]["count"] += 1
        return list(heatmap.values())

    async def get_metric_average(
        self, athlete_id: UUID, metric_type: str, days: int = 7
    ) -> Optional[float]:
        model = _METRIC_MODELS.get(metric_type)
        if not model:
            return None

        start_date = datetime.utcnow() - timedelta(days=days)
        result = await self.db.execute(
            select(model).filter(
                model.athlete_id == athlete_id,
                model.recorded_at >= start_date,
            )
        )
        metrics = list(result.scalars().all())
        if not metrics:
            return None
        return sum(m.value for m in metrics) / len(metrics)

    async def get_global_summary(self) -> Dict:
        """Real platform-wide stats for the dashboard."""
        # All athletes
        athletes_result = await self.db.execute(select(Athlete))
        athletes = list(athletes_result.scalars().all())
        total_athletes = len(athletes)

        # All sessions + time-bounded counts
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())

        sessions_result = await self.db.execute(select(TrainingSession))
        all_sessions = list(sessions_result.scalars().all())
        total_sessions = len(all_sessions)
        sessions_today = sum(1 for s in all_sessions if s.completed_at >= today_start)
        sessions_this_week = sum(1 for s in all_sessions if s.completed_at >= week_start)

        # Most active athlete this week (by session count)
        weekly_sessions = [s for s in all_sessions if s.completed_at >= week_start]
        most_active_name: Optional[str] = None
        if weekly_sessions and athletes:
            from collections import Counter
            counts = Counter(str(s.athlete_id) for s in weekly_sessions)
            top_id = counts.most_common(1)[0][0]
            top_athlete = next((a for a in athletes if str(a.id) == top_id), None)
            most_active_name = top_athlete.name if top_athlete else None

        return {
            "total_athletes": total_athletes,
            "total_training_sessions": total_sessions,
            "sessions_today": sessions_today,
            "sessions_this_week": sessions_this_week,
            "most_active_athlete": most_active_name,
        }

    async def get_team_summary(self) -> List[Dict]:
        """Bulk athlete summaries — avoids N×8 requests from the frontend."""
        athletes_result = await self.db.execute(select(Athlete))
        athletes = list(athletes_result.scalars().all())
        if not athletes:
            return []

        # Fetch all summaries in parallel
        summaries = await asyncio.gather(
            *[self.get_athlete_summary(athlete.id) for athlete in athletes]
        )
        return [s for s in summaries if s is not None]
