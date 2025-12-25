from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from ..database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    source_type = Column(String, nullable=False) # e.g., "SMS", "Twitter", "Email"
    source_identifier = Column(String, nullable=True) # e.g., phone number, handle
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String, default="Pending") # "Pending", "Verified", "Rejected"
    disaster_category = Column(String, nullable=True) # Populated by AI
    location = Column(String, nullable=True)
