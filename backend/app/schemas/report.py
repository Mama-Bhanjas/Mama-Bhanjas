from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportBase(BaseModel):
    text: str
    source_type: str
    source_identifier: Optional[str] = None
    location: Optional[str] = None

class ReportCreate(ReportBase):
    disaster_category: Optional[str] = None

class ReportResponse(ReportBase):
    id: int
    timestamp: datetime
    is_verified: bool
    verification_status: str
    disaster_category: Optional[str] = None

    class Config:
        from_attributes = True
