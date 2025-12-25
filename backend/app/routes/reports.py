from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.report import Report
from ..schemas.report import ReportCreate, ReportResponse
from ..services.verification import VerificationService
from ..services.ai_pipeline import ai_pipeline

router = APIRouter()

@router.post("/", response_model=ReportResponse)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    # 2. Unified AI Processing
    # Calls classification, summarization, NER, and verification in one go
    ai_result = ai_pipeline.process_report(report.text, report.source_identifier)
    
    # Defaults
    category = "Other"
    location = report.location  # Start with user-provided location
    verification_status = "Pending"
    is_verified = False
    text_to_store = report.text  # Default to original text

    if ai_result.get("success") and ai_result.get("data"):
        data = ai_result["data"]
        
        # If URL was extracted, use the extracted text or summary instead of URL
        if data.get("extraction_method") == "url" and data.get("extracted_text"):
            # Use summary if available (more concise), otherwise use extracted text
            text_to_store = data.get("summary") or data.get("extracted_text")
        
        # 1. Category: Prefer user input, fallback to AI 'primary_category' or 'disaster_type'
        if report.disaster_category:
            category = report.disaster_category
        else:
            category = data.get("primary_category") or data.get("disaster_type") or "Other"

        # 2. Location: Prefer user input, fallback to AI extracted location
        # Only use AI location if user didn't provide one
        if not location and data.get("location_entities") and len(data["location_entities"]) > 0:
            # Take the first location entity found
            location = data["location_entities"][0]
        
        # 3. Verification status from AI
        verification_data = data.get("verification", {})
        if verification_data.get("status"):
            verification_status = verification_data["status"]
            is_verified = verification_data.get("is_reliable", False)

    db_report = Report(
        text=text_to_store,  # Use extracted/summarized text instead of URL
        source_type=report.source_type,
        source_identifier=report.source_identifier,
        location=location,
        is_verified=is_verified,
        verification_status=verification_status,
        disaster_category=category
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/{report_id}", response_model=ReportResponse)
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@router.get("/", response_model=List[ReportResponse])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reports = db.query(Report).offset(skip).limit(limit).all()
    return reports
