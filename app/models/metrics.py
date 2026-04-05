from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Uuid
from sqlalchemy.sql import func
from datetime import datetime
from uuid import uuid4
from app.db.base import Base


class SpeedMetric(Base):
    __tablename__ = "speed_metrics"

    id = Column(Uuid, primary_key=True, default=uuid4)
    athlete_id = Column(Uuid, ForeignKey("athletes.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class StaminaMetric(Base):
    __tablename__ = "stamina_metrics"

    id = Column(Uuid, primary_key=True, default=uuid4)
    athlete_id = Column(Uuid, ForeignKey("athletes.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class StrengthMetric(Base):
    __tablename__ = "strength_metrics"

    id = Column(Uuid, primary_key=True, default=uuid4)
    athlete_id = Column(Uuid, ForeignKey("athletes.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class HeartRateMetric(Base):
    __tablename__ = "heart_rate_metrics"

    id = Column(Uuid, primary_key=True, default=uuid4)
    athlete_id = Column(Uuid, ForeignKey("athletes.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class VO2MaxMetric(Base):
    __tablename__ = "vo2_max_metrics"

    id = Column(Uuid, primary_key=True, default=uuid4)
    athlete_id = Column(Uuid, ForeignKey("athletes.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SleepMetric(Base):
    __tablename__ = "sleep_metrics"

    id = Column(Uuid, primary_key=True, default=uuid4)
    athlete_id = Column(Uuid, ForeignKey("athletes.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class RecoveryMetric(Base):
    __tablename__ = "recovery_metrics"

    id = Column(Uuid, primary_key=True, default=uuid4)
    athlete_id = Column(Uuid, ForeignKey("athletes.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class FatigueMetric(Base):
    __tablename__ = "fatigue_metrics"

    id = Column(Uuid, primary_key=True, default=uuid4)
    athlete_id = Column(Uuid, ForeignKey("athletes.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
