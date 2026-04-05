#!/usr/bin/env python3
"""Initialize database with all tables."""

from app.db.base import Base, engine
from app.models import (
    Athlete,
    SpeedMetric, StaminaMetric, StrengthMetric, HeartRateMetric,
    VO2MaxMetric, SleepMetric, RecoveryMetric, FatigueMetric,
    TrainingSession,
    User, OTP
)


def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully")


if __name__ == "__main__":
    init_db()
