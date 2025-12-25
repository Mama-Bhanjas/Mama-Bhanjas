from sqlalchemy import Column, Integer, String, Text, Float, JSON
from ..database import Base

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    summary_text = Column(Text, nullable=False)
    reputation_score = Column(Float, default=0.0)
    report_ids = Column(JSON, nullable=True) # Storing list of report IDs that contributed to this summary
