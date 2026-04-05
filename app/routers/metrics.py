from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.base import get_db
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
from app.services.metrics import (
    SpeedMetricService, StaminaMetricService, StrengthMetricService,
    HeartRateMetricService, VO2MaxMetricService, SleepMetricService,
    RecoveryMetricService, FatigueMetricService,
)

router = APIRouter(prefix="/athletes/{athlete_id}/metrics", tags=["metrics"])


# ── Speed ─────────────────────────────────────────────────────────────────────
@router.post("/speed", response_model=SpeedMetricResponse)
async def create_speed_metric(athlete_id: UUID, metric: SpeedMetricCreate, db: AsyncSession = Depends(get_db)):
    return await SpeedMetricService(db).create(athlete_id, metric)

@router.get("/speed", response_model=List[SpeedMetricResponse])
async def get_speed_metrics(athlete_id: UUID, limit: int = Query(100, ge=1, le=1000), db: AsyncSession = Depends(get_db)):
    return await SpeedMetricService(db).get_by_athlete(athlete_id, limit)

@router.get("/speed/latest", response_model=SpeedMetricResponse)
async def get_latest_speed_metric(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = await SpeedMetricService(db).get_latest(athlete_id)
    if not metric:
        raise HTTPException(status_code=404, detail="No speed metrics found")
    return metric


# ── Stamina ───────────────────────────────────────────────────────────────────
@router.post("/stamina", response_model=StaminaMetricResponse)
async def create_stamina_metric(athlete_id: UUID, metric: StaminaMetricCreate, db: AsyncSession = Depends(get_db)):
    return await StaminaMetricService(db).create(athlete_id, metric)

@router.get("/stamina", response_model=List[StaminaMetricResponse])
async def get_stamina_metrics(athlete_id: UUID, limit: int = Query(100, ge=1, le=1000), db: AsyncSession = Depends(get_db)):
    return await StaminaMetricService(db).get_by_athlete(athlete_id, limit)

@router.get("/stamina/latest", response_model=StaminaMetricResponse)
async def get_latest_stamina_metric(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = await StaminaMetricService(db).get_latest(athlete_id)
    if not metric:
        raise HTTPException(status_code=404, detail="No stamina metrics found")
    return metric


# ── Strength ──────────────────────────────────────────────────────────────────
@router.post("/strength", response_model=StrengthMetricResponse)
async def create_strength_metric(athlete_id: UUID, metric: StrengthMetricCreate, db: AsyncSession = Depends(get_db)):
    return await StrengthMetricService(db).create(athlete_id, metric)

@router.get("/strength", response_model=List[StrengthMetricResponse])
async def get_strength_metrics(athlete_id: UUID, limit: int = Query(100, ge=1, le=1000), db: AsyncSession = Depends(get_db)):
    return await StrengthMetricService(db).get_by_athlete(athlete_id, limit)

@router.get("/strength/latest", response_model=StrengthMetricResponse)
async def get_latest_strength_metric(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = await StrengthMetricService(db).get_latest(athlete_id)
    if not metric:
        raise HTTPException(status_code=404, detail="No strength metrics found")
    return metric


# ── Heart Rate  (routes: heart-rate | heart_rate both work via frontend mapper) ──
@router.post("/heart-rate", response_model=HeartRateMetricResponse)
async def create_heart_rate_metric(athlete_id: UUID, metric: HeartRateMetricCreate, db: AsyncSession = Depends(get_db)):
    return await HeartRateMetricService(db).create(athlete_id, metric)

@router.get("/heart-rate", response_model=List[HeartRateMetricResponse])
async def get_heart_rate_metrics(athlete_id: UUID, limit: int = Query(100, ge=1, le=1000), db: AsyncSession = Depends(get_db)):
    return await HeartRateMetricService(db).get_by_athlete(athlete_id, limit)

@router.get("/heart-rate/latest", response_model=HeartRateMetricResponse)
async def get_latest_heart_rate_metric(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = await HeartRateMetricService(db).get_latest(athlete_id)
    if not metric:
        raise HTTPException(status_code=404, detail="No heart rate metrics found")
    return metric


# ── VO2 Max  (routes: vo2-max | vo2_max both work via frontend mapper) ─────────
@router.post("/vo2-max", response_model=VO2MaxMetricResponse)
async def create_vo2_max_metric(athlete_id: UUID, metric: VO2MaxMetricCreate, db: AsyncSession = Depends(get_db)):
    return await VO2MaxMetricService(db).create(athlete_id, metric)

@router.get("/vo2-max", response_model=List[VO2MaxMetricResponse])
async def get_vo2_max_metrics(athlete_id: UUID, limit: int = Query(100, ge=1, le=1000), db: AsyncSession = Depends(get_db)):
    return await VO2MaxMetricService(db).get_by_athlete(athlete_id, limit)

@router.get("/vo2-max/latest", response_model=VO2MaxMetricResponse)
async def get_latest_vo2_max_metric(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = await VO2MaxMetricService(db).get_latest(athlete_id)
    if not metric:
        raise HTTPException(status_code=404, detail="No VO2 max metrics found")
    return metric


# ── Sleep ─────────────────────────────────────────────────────────────────────
@router.post("/sleep", response_model=SleepMetricResponse)
async def create_sleep_metric(athlete_id: UUID, metric: SleepMetricCreate, db: AsyncSession = Depends(get_db)):
    return await SleepMetricService(db).create(athlete_id, metric)

@router.get("/sleep", response_model=List[SleepMetricResponse])
async def get_sleep_metrics(athlete_id: UUID, limit: int = Query(100, ge=1, le=1000), db: AsyncSession = Depends(get_db)):
    return await SleepMetricService(db).get_by_athlete(athlete_id, limit)

@router.get("/sleep/latest", response_model=SleepMetricResponse)
async def get_latest_sleep_metric(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = await SleepMetricService(db).get_latest(athlete_id)
    if not metric:
        raise HTTPException(status_code=404, detail="No sleep metrics found")
    return metric


# ── Recovery ──────────────────────────────────────────────────────────────────
@router.post("/recovery", response_model=RecoveryMetricResponse)
async def create_recovery_metric(athlete_id: UUID, metric: RecoveryMetricCreate, db: AsyncSession = Depends(get_db)):
    return await RecoveryMetricService(db).create(athlete_id, metric)

@router.get("/recovery", response_model=List[RecoveryMetricResponse])
async def get_recovery_metrics(athlete_id: UUID, limit: int = Query(100, ge=1, le=1000), db: AsyncSession = Depends(get_db)):
    return await RecoveryMetricService(db).get_by_athlete(athlete_id, limit)

@router.get("/recovery/latest", response_model=RecoveryMetricResponse)
async def get_latest_recovery_metric(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = await RecoveryMetricService(db).get_latest(athlete_id)
    if not metric:
        raise HTTPException(status_code=404, detail="No recovery metrics found")
    return metric


# ── Fatigue ───────────────────────────────────────────────────────────────────
@router.post("/fatigue", response_model=FatigueMetricResponse)
async def create_fatigue_metric(athlete_id: UUID, metric: FatigueMetricCreate, db: AsyncSession = Depends(get_db)):
    return await FatigueMetricService(db).create(athlete_id, metric)

@router.get("/fatigue", response_model=List[FatigueMetricResponse])
async def get_fatigue_metrics(athlete_id: UUID, limit: int = Query(100, ge=1, le=1000), db: AsyncSession = Depends(get_db)):
    return await FatigueMetricService(db).get_by_athlete(athlete_id, limit)

@router.get("/fatigue/latest", response_model=FatigueMetricResponse)
async def get_latest_fatigue_metric(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = await FatigueMetricService(db).get_latest(athlete_id)
    if not metric:
        raise HTTPException(status_code=404, detail="No fatigue metrics found")
    return metric
