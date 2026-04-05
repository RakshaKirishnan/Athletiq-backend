"""Metric services — async SQLAlchemy."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from uuid import UUID
from typing import Type, Generic, TypeVar, List, Optional

from app.models.metrics import (
    SpeedMetric, StaminaMetric, StrengthMetric, HeartRateMetric,
    VO2MaxMetric, SleepMetric, RecoveryMetric, FatigueMetric,
)
from app.schemas.metrics import (
    SpeedMetricCreate, SpeedMetricResponse,
    StaminaMetricCreate, StaminaMetricResponse,
    StrengthMetricCreate, StrengthMetricResponse,
    HeartRateMetricCreate, HeartRateMetricResponse,
    VO2MaxMetricCreate, VO2MaxMetricResponse,
    SleepMetricCreate, SleepMetricResponse,
    RecoveryMetricCreate, RecoveryMetricResponse,
    FatigueMetricCreate, FatigueMetricResponse,
)

T = TypeVar("T")
CreateT = TypeVar("CreateT")
ResponseT = TypeVar("ResponseT")


class BaseMetricService(Generic[T, CreateT, ResponseT]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def create(self, athlete_id: UUID, metric: CreateT) -> ResponseT:
        db_metric = self.model(
            athlete_id=athlete_id,
            value=metric.value,
            unit=metric.unit,
            notes=getattr(metric, "notes", None),
        )
        self.db.add(db_metric)
        await self.db.commit()
        await self.db.refresh(db_metric)
        return db_metric

    async def get_by_id(self, metric_id: UUID) -> Optional[T]:
        result = await self.db.execute(
            select(self.model).filter(self.model.id == metric_id)
        )
        return result.scalars().first()

    async def get_by_athlete(self, athlete_id: UUID, limit: int = 100) -> List[T]:
        result = await self.db.execute(
            select(self.model)
            .filter(self.model.athlete_id == athlete_id)
            .order_by(self.model.recorded_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_athlete_date_range(
        self,
        athlete_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> List[T]:
        result = await self.db.execute(
            select(self.model).filter(
                self.model.athlete_id == athlete_id,
                self.model.recorded_at >= start_date,
                self.model.recorded_at <= end_date,
            ).order_by(self.model.recorded_at.desc())
        )
        return list(result.scalars().all())

    async def get_latest(self, athlete_id: UUID) -> Optional[T]:
        result = await self.db.execute(
            select(self.model)
            .filter(self.model.athlete_id == athlete_id)
            .order_by(self.model.recorded_at.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def delete(self, metric_id: UUID) -> bool:
        metric = await self.get_by_id(metric_id)
        if not metric:
            return False
        await self.db.delete(metric)
        await self.db.commit()
        return True

    async def get_average(self, athlete_id: UUID, days: int = 7) -> Optional[float]:
        start_date = datetime.utcnow() - timedelta(days=days)
        metrics = await self.get_by_athlete_date_range(
            athlete_id, start_date, datetime.utcnow()
        )
        if not metrics:
            return None
        return sum(m.value for m in metrics) / len(metrics)


class SpeedMetricService(BaseMetricService[SpeedMetric, SpeedMetricCreate, SpeedMetricResponse]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, SpeedMetric)


class StaminaMetricService(BaseMetricService[StaminaMetric, StaminaMetricCreate, StaminaMetricResponse]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, StaminaMetric)


class StrengthMetricService(BaseMetricService[StrengthMetric, StrengthMetricCreate, StrengthMetricResponse]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, StrengthMetric)


class HeartRateMetricService(BaseMetricService[HeartRateMetric, HeartRateMetricCreate, HeartRateMetricResponse]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, HeartRateMetric)


class VO2MaxMetricService(BaseMetricService[VO2MaxMetric, VO2MaxMetricCreate, VO2MaxMetricResponse]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, VO2MaxMetric)


class SleepMetricService(BaseMetricService[SleepMetric, SleepMetricCreate, SleepMetricResponse]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, SleepMetric)


class RecoveryMetricService(BaseMetricService[RecoveryMetric, RecoveryMetricCreate, RecoveryMetricResponse]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, RecoveryMetric)


class FatigueMetricService(BaseMetricService[FatigueMetric, FatigueMetricCreate, FatigueMetricResponse]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, FatigueMetric)
