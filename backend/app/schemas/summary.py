from pydantic import BaseModel
from typing import List, Optional

class SummaryBase(BaseModel):
    category: str
    summary_text: str
    reputation_score: float

class SummaryResponse(SummaryBase):
    id: int
    report_ids: Optional[List[int]] = []

    class Config:
        from_attributes = True
