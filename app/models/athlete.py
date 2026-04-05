from sqlalchemy import Column, String, Integer, Float, Uuid
from uuid import uuid4
from app.db.base import Base


class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(Uuid, primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    sport = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    team = Column(String(255), nullable=True)
