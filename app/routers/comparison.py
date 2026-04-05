from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.base import get_db
from app.schemas.comparison import AthleteMetricComparison, RadarComparisonData
from app.services.comparison import ComparisonService

router = APIRouter(prefix="/comparison", tags=["comparison"])


@router.get("/radar", response_model=List[RadarComparisonData])
async def get_radar_comparison(
    athlete_ids: List[UUID] = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db),
):
    return await ComparisonService(db).get_radar_comparison(athlete_ids)


@router.get("/metrics/{metric_type}", response_model=List[AthleteMetricComparison])
async def compare_metric(
    metric_type: str,
    athlete_ids: List[UUID] = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db),
):
    return await ComparisonService(db).get_metric_comparison(athlete_ids, metric_type)
