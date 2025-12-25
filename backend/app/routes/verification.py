from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.ai_pipeline import ai_pipeline

router = APIRouter()

class VerifyRequest(BaseModel):
    text: str
    source_url: Optional[str] = None

@router.post("/news")
async def verify_news(request: VerifyRequest):
    result = ai_pipeline.verify_news(request.text, request.source_url)
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result

@router.post("/report")
async def verify_report(request: VerifyRequest):
    result = ai_pipeline.verify_report(request.text)
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result

@router.post("/factcheck")
async def fact_check(request: VerifyRequest):
    """
    Deep verification/fact check
    """
    result = ai_pipeline.fact_check(request.text)
    # Fact check pipeline might return success=True/False or just dict
    # We pass it through
    return result
