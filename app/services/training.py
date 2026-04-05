"""Training session service — async SQLAlchemy."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Optional

from app.models.training import TrainingSession
from app.schemas.training import TrainingSessionCreate, TrainingSessionUpdate


class TrainingSessionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, session: TrainingSessionCreate) -> TrainingSession:
        db_session = TrainingSession(**session.model_dump())
        self.db.add(db_session)
        await self.db.commit()
        await self.db.refresh(db_session)
        return db_session

    async def get_by_id(self, session_id: UUID) -> Optional[TrainingSession]:
        result = await self.db.execute(
            select(TrainingSession).filter(TrainingSession.id == session_id)
        )
        return result.scalars().first()

    async def get_by_athlete(
        self, athlete_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[TrainingSession]:
        result = await self.db.execute(
            select(TrainingSession)
            .filter(TrainingSession.athlete_id == athlete_id)
            .order_by(TrainingSession.completed_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_athlete_date_range(
        self, athlete_id: UUID, start_date: datetime, end_date: datetime
    ) -> List[TrainingSession]:
        result = await self.db.execute(
            select(TrainingSession).filter(
                TrainingSession.athlete_id == athlete_id,
                TrainingSession.completed_at >= start_date,
                TrainingSession.completed_at <= end_date,
            ).order_by(TrainingSession.completed_at.desc())
        )
        return list(result.scalars().all())

    async def update(
        self, session_id: UUID, session: TrainingSessionUpdate
    ) -> Optional[TrainingSession]:
        db_session = await self.get_by_id(session_id)
        if not db_session:
            return None
        for field, value in session.model_dump(exclude_unset=True).items():
            setattr(db_session, field, value)
        await self.db.commit()
        await self.db.refresh(db_session)
        return db_session

    async def delete(self, session_id: UUID) -> bool:
        db_session = await self.get_by_id(session_id)
        if not db_session:
            return False
        await self.db.delete(db_session)
        await self.db.commit()
        return True

    async def get_total_calories(self, athlete_id: UUID, days: int = 7) -> float:
        start_date = datetime.utcnow() - timedelta(days=days)
        sessions = await self.get_by_athlete_date_range(
            athlete_id, start_date, datetime.utcnow()
        )
        return sum(s.calories_burned or 0 for s in sessions)

    async def get_total_duration(self, athlete_id: UUID, days: int = 7) -> float:
        start_date = datetime.utcnow() - timedelta(days=days)
        sessions = await self.get_by_athlete_date_range(
            athlete_id, start_date, datetime.utcnow()
        )
        return sum(s.duration_minutes for s in sessions)
