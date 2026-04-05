#!/usr/bin/env python3
"""
Initialize database — creates all tables using the async SQLAlchemy engine.

Usage:
    source .venv/bin/activate          # Mac/Linux
    .venv\\Scripts\\activate             # Windows
    python init_db.py
"""

import asyncio
from app.db.base import Base, engine

# Import all models so SQLAlchemy knows about them before create_all
from app.models import (  # noqa: F401
    Athlete,
    SpeedMetric, StaminaMetric, StrengthMetric, HeartRateMetric,
    VO2MaxMetric, SleepMetric, RecoveryMetric, FatigueMetric,
    TrainingSession,
    User, OTP,
)


async def init_db() -> None:
    print("Creating database tables...")
    async with engine.begin() as conn:
        # run_sync bridges the async connection to the sync create_all API
        await conn.run_sync(Base.metadata.create_all)
    print("✓ All tables created successfully")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
