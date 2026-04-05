from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.base import get_db
from app.schemas.analytics import AthleteSummary, TrendPoint, HeatmapData, GlobalSummary, AthleteTeamSummary
from app.services.analytics import AnalyticsService

# Per-athlete analytics (prefixed with /athletes/{athlete_id}/analytics)
router = APIRouter(prefix="/athletes/{athlete_id}/analytics", tags=["analytics"])


@router.get("/summary", response_model=AthleteSummary)
async def get_analytics_summary(athlete_id: UUID, db: AsyncSession = Depends(get_db)):
    service = AnalyticsService(db)
    summary = await service.get_athlete_summary(athlete_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return summary


@router.get("/trends/{metric_type}", response_model=List[TrendPoint])
async def get_metric_trends(
    athlete_id: UUID,
    metric_type: str,
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    return await AnalyticsService(db).get_metric_trends(athlete_id, metric_type, days)


@router.get("/heatmap", response_model=List[HeatmapData])
async def get_training_heatmap(
    athlete_id: UUID,
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    return await AnalyticsService(db).get_training_heatmap(athlete_id, days)


@router.get("/average/{metric_type}")
async def get_metric_average(
    athlete_id: UUID,
    metric_type: str,
    days: int = Query(7, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    average = await AnalyticsService(db).get_metric_average(athlete_id, metric_type, days)
    if average is None:
        raise HTTPException(status_code=404, detail="No data found for metric")
    return {"metric_type": metric_type, "average": average, "days": days}


# ── Platform-wide analytics (no athlete_id prefix) ──────────────────────────
platform_router = APIRouter(prefix="/analytics", tags=["analytics"])


@platform_router.get("/global-summary", response_model=GlobalSummary)
async def get_global_summary(db: AsyncSession = Depends(get_db)):
    """Platform-wide real stats for the dashboard."""
    return await AnalyticsService(db).get_global_summary()


@platform_router.get("/team-summary", response_model=List[AthleteTeamSummary])
async def get_team_summary(db: AsyncSession = Depends(get_db)):
    """Bulk athlete summaries — one request instead of N×8."""
    return await AnalyticsService(db).get_team_summary()
