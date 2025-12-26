from fastapi import APIRouter, HTTPException, status
from ..services.ai_pipeline import ai_pipeline

router = APIRouter()

@router.get("/realtime", response_model=dict)
async def get_realtime_news():
    """
    Get the latest AI-processed disaster news for Nepal.
    Proxies the request to the AI Service's cache.
    """
    try:
        result = ai_pipeline.get_realtime_news()
        if not result.get("success", True): # Handle downstream errors conservatively
             # If the AI service explicitly returns success=False
             raise HTTPException(status_code=502, detail=result.get("error", "AI Service returned failure."))
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
@router.get("/sync", response_model=dict)
async def sync_intelligence():
    """
    Manually trigger the AI Service to fetch and process all multi-source news.
    """
    try:
        # Proxy to AI Service API
        import requests
        from ..config import settings
        response = requests.get(f"{settings.AI_SERVICE_URL}/api/fetch/all")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
