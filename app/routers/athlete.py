from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.base import get_db
from app.schemas.athlete import AthleteCreate, AthleteUpdate, AthleteResponse
from app.services.athlete import AthleteService

router = APIRouter(prefix="/athletes", tags=["athletes"])


@router.post("", response_model=AthleteResponse)
async def create_athlete(athlete: AthleteCreate, db: AsyncSession = Depends(get_db)):
    service = AthleteService(db)
    return await service.create(athlete)


@router.get("", response_model=List[AthleteResponse])
async def list_athletes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    service = AthleteService(db)
    return await service.list_all(skip, limit)


@router.get("/{athlete_id}", response_model=AthleteResponse)
async def get_athlete(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    service = AthleteService(db)
    athlete = await service.get_by_id(athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return athlete


@router.put("/{athlete_id}", response_model=AthleteResponse)
async def update_athlete(
    athlete_id: UUID,
    athlete: AthleteUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = AthleteService(db)
    updated = await service.update(athlete_id, athlete)
    if not updated:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return updated


@router.delete("/{athlete_id}")
async def delete_athlete(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    service = AthleteService(db)
    if not await service.delete(athlete_id):
        raise HTTPException(status_code=404, detail="Athlete not found")
    return {"detail": "Athlete deleted"}
