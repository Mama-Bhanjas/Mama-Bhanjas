from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

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
    summary = None
    confidence_score = None

    if ai_result.get("success") and ai_result.get("data"):
        data = ai_result["data"]
        
        # If URL was extracted, use the extracted text or summary instead of URL
        if data.get("extraction_method") == "url" and data.get("extracted_text"):
            # Use summary if available (more concise), otherwise use extracted text
            text_to_store = data.get("summary") or data.get("extracted_text")
        
        # Extract AI-generated summary
        summary = data.get("summary")
        
        # Extract confidence score from classification
        if data.get("confidence"):
            confidence_score = data.get("confidence")
        
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
        
        if data.get("verification", {}).get("status"):
            verification_status = data["verification"]["status"]
            is_verified = data["verification"].get("is_reliable", False)

    # Title Logic: Prefer user input, then AI extracted title, then summary fallback
    title_to_store = report.title
    if not title_to_store:
        if data.get("title"):
             title_to_store = data.get("title")
        elif summary:
             # Use first sentence of summary
             title_to_store = summary.split('.')[0][:80]
             if len(summary) > 80: title_to_store += "..."
        else:
             title_to_store = f"{category} Report"

    db_report = Report(
        title=title_to_store,
        text=text_to_store,  # Use extracted/summarized text instead of URL
        source_type=report.source_type,
        source_identifier=report.source_identifier,
        location=location,
        is_verified=is_verified,
        verification_status=verification_status,
        disaster_category=category,
        submitted_by=report.submitted_by or "Anonymous",
        summary=summary,
        confidence_score=confidence_score
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.post("/upload", response_model=ReportResponse)
async def upload_pdf_report(
    file: UploadFile = File(...),
    disaster_category: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    submitted_by: Optional[str] = Form("Anonymous"),
    db: Session = Depends(get_db)
):
    # 1. Read file content
    content = await file.read()
    
    # 2. Call AI Service for PDF Processing
    ai_result = ai_pipeline.upload_report(content, file.filename)
    
    if not ai_result.get("success"):
        raise HTTPException(status_code=500, detail=ai_result.get("error", "AI Upload Failed"))

    data = ai_result["data"]
    
    # Defaults
    category = disaster_category or data.get("primary_category") or data.get("disaster_type") or "Other"
    loc = location
    # If user didn't provide location, use AI extracted one
    if not loc and data.get("location_entities") and len(data["location_entities"]) > 0:
        loc = data["location_entities"][0]
        
    verification_status = "Pending"
    is_verified = False
    summary = data.get("summary")
    confidence_score = data.get("confidence")
    
    verification_data = data.get("verification", {})
    if verification_data.get("status"):
        verification_status = verification_data["status"]
        is_verified = verification_data.get("is_reliable", False)

    # Title Logic for PDF
    title_to_store = data.get("title")
    if not title_to_store:
        if summary:
            title_to_store = summary.split('.')[0][:80]
        else:
            title_to_store = f"PDF Report: {file.filename}"

    # 3. Store in DB
    db_report = Report(
        title=title_to_store,
        text=data.get("summary") or data.get("extracted_text") or f"PDF: {file.filename}",
        source_type="PDF_UPLOAD",
        source_identifier=file.filename,
        location=loc,
        is_verified=is_verified,
        verification_status=verification_status,
        disaster_category=category,
        submitted_by=submitted_by,
        summary=summary,
        confidence_score=confidence_score
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
