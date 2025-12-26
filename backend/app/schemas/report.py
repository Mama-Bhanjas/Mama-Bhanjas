from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportBase(BaseModel):
    text: str
    source_type: str
    source_identifier: Optional[str] = None
    location: Optional[str] = None

class ReportCreate(ReportBase):
    title: Optional[str] = None
    disaster_category: Optional[str] = None
    submitted_by: Optional[str] = "Anonymous"

class ReportResponse(ReportBase):
    id: int
    title: Optional[str] = None
    timestamp: datetime
    is_verified: bool
    verification_status: str
    disaster_category: Optional[str] = None
    submitted_by: Optional[str] = None
    summary: Optional[str] = None
    confidence_score: Optional[float] = None

    class Config:
        from_attributes = True
