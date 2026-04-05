"""Athlete CRUD service — async SQLAlchemy."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List, Optional

from app.models.athlete import Athlete
from app.schemas.athlete import AthleteCreate, AthleteUpdate


class AthleteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, athlete: AthleteCreate) -> Athlete:
        db_athlete = Athlete(**athlete.model_dump())
        self.db.add(db_athlete)
        await self.db.commit()
        await self.db.refresh(db_athlete)
        return db_athlete

    async def get_by_id(self, athlete_id: UUID) -> Optional[Athlete]:
        result = await self.db.execute(select(Athlete).filter(Athlete.id == athlete_id))
        return result.scalars().first()

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Athlete]:
        result = await self.db.execute(select(Athlete).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, athlete_id: UUID, athlete: AthleteUpdate) -> Optional[Athlete]:
        db_athlete = await self.get_by_id(athlete_id)
        if not db_athlete:
            return None
        for field, value in athlete.model_dump(exclude_unset=True).items():
            setattr(db_athlete, field, value)
        await self.db.commit()
        await self.db.refresh(db_athlete)
        return db_athlete

    async def delete(self, athlete_id: UUID) -> bool:
        db_athlete = await self.get_by_id(athlete_id)
        if not db_athlete:
            return False
        await self.db.delete(db_athlete)
        await self.db.commit()
        return True
