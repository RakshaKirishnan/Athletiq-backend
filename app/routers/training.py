from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.base import get_db
from app.schemas.training import TrainingSessionCreate, TrainingSessionUpdate, TrainingSessionResponse
from app.services.training import TrainingSessionService

router = APIRouter(prefix="/athletes/{athlete_id}/training-sessions", tags=["training"])


@router.post("", response_model=TrainingSessionResponse)
async def create_training_session(
    athlete_id: UUID,
    session: TrainingSessionCreate,
    db: AsyncSession = Depends(get_db),
):
    return await TrainingSessionService(db).create(session)


@router.get("", response_model=List[TrainingSessionResponse])
async def list_training_sessions(
    athlete_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    return await TrainingSessionService(db).get_by_athlete(athlete_id, skip, limit)


@router.get("/{session_id}", response_model=TrainingSessionResponse)
async def get_training_session(
    athlete_id: UUID,
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    session = await TrainingSessionService(db).get_by_id(session_id)
    if not session or session.athlete_id != athlete_id:
        raise HTTPException(status_code=404, detail="Training session not found")
    return session


@router.put("/{session_id}", response_model=TrainingSessionResponse)
async def update_training_session(
    athlete_id: UUID,
    session_id: UUID,
    session: TrainingSessionUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = TrainingSessionService(db)
    existing = await service.get_by_id(session_id)
    if not existing or existing.athlete_id != athlete_id:
        raise HTTPException(status_code=404, detail="Training session not found")
    return await service.update(session_id, session)


@router.delete("/{session_id}")
async def delete_training_session(
    athlete_id: UUID,
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = TrainingSessionService(db)
    existing = await service.get_by_id(session_id)
    if not existing or existing.athlete_id != athlete_id:
        raise HTTPException(status_code=404, detail="Training session not found")
    await service.delete(session_id)
    return {"detail": "Training session deleted"}
