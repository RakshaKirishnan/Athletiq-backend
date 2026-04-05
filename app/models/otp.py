from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from uuid import uuid4
from app.db.base import Base


class OTP(Base):
    __tablename__ = "otps"

    otp_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), nullable=False, index=True)
    otp_code = Column(String(6), nullable=False)
    purpose = Column(String(50), nullable=False)  # signup, login, password_reset
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
