from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class AthleteBase(BaseModel):
    name: str
    age: Optional[int] = None
    sport: Optional[str] = None
    position: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    team: Optional[str] = None


class AthleteCreate(AthleteBase):
    pass


class AthleteUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    sport: Optional[str] = None
    position: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    team: Optional[str] = None


class AthleteResponse(AthleteBase):
    id: UUID

    class Config:
        from_attributes = True
