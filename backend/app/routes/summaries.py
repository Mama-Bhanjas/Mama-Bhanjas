from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.report import Report
from ..models.summary import Summary
from ..schemas.summary import SummaryResponse
from ..services.ai_pipeline import ai_pipeline

router = APIRouter()

@router.get("/", response_model=List[SummaryResponse])
def get_summaries(db: Session = Depends(get_db)):
    # In a real system, this would be a background job.
    # Here, we generate summaries on the fly for demonstration.
    
    # Group reports by category
    reports = db.query(Report).all()
    grouped_reports = {}
    for report in reports:
        if report.disaster_category not in grouped_reports:
            grouped_reports[report.disaster_category] = []
        grouped_reports[report.disaster_category].append(report)
        
    response_summaries = []
    
    print(f"DEBUG: Grouped reports categories: {list(grouped_reports.keys())}")
    
    for category, category_reports in grouped_reports.items():
        if not category_reports:
            continue

        print(f"DEBUG: Processing category: {category}")
        report_texts = [r.text for r in category_reports]
        summary_text = ai_pipeline.summarize_reports(report_texts)
        
        # Simple reputation score calculation based on verified count
        verified_count = sum(1 for r in category_reports if r.is_verified)
        total_count = len(category_reports)
        reputation_score = (verified_count / total_count) * 10 if total_count > 0 else 0
        
        report_ids = [r.id for r in category_reports]
        
        # Use a more stable integer ID (hash() can be negative which Pydantic might dislike)
        mock_id = abs(hash(category)) % 1000000
        
        summary = SummaryResponse(
            id=mock_id,
            category=category,
            summary_text=summary_text,
            reputation_score=reputation_score,
            report_ids=report_ids
        )
        response_summaries.append(summary)
        
    print(f"DEBUG: Returning {len(response_summaries)} summaries")
    return response_summaries
