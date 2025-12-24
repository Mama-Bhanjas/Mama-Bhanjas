"""
FastAPI-based API for AI Service
Exposes ML endpoints for classification, summarization, and clustering
"""
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

from ai_service.pipelines.classify import ClassificationPipeline
from ai_service.pipelines.summarize import SummarizationPipeline
from ai_service.pipelines.cluster import ClusteringPipeline
from ai_service.utils import setup_logging


# Initialize logging
setup_logging(log_level="INFO")

# Initialize FastAPI app
app = FastAPI(
    title="AI Service API",
    description="ML endpoints for report classification, summarization, and clustering",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipelines (lazy loading)
classification_pipeline = None
summarization_pipeline = None
clustering_pipeline = None


# Request/Response Models
class ClassifyRequest(BaseModel):
    text: str = Field(..., description="Text to classify", min_length=10)
    top_k: int = Field(3, description="Number of top categories to return", ge=1, le=10)
    threshold: float = Field(0.1, description="Minimum confidence threshold", ge=0.0, le=1.0)


class ClassifyResponse(BaseModel):
    success: bool
    category: Optional[str]
    confidence: float
    top_categories: List[dict]
    text_length: Optional[int]
    error: Optional[str] = None


class BatchClassifyRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to classify")
    top_k: int = Field(3, ge=1, le=10)
    threshold: float = Field(0.1, ge=0.0, le=1.0)


class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Text to summarize", min_length=50)
    max_length: int = Field(150, description="Maximum summary length", ge=30, le=500)
    min_length: int = Field(30, description="Minimum summary length", ge=10, le=200)


class SummarizeResponse(BaseModel):
    success: bool
    summary: str
    original_length: Optional[int]
    summary_length: Optional[int]
    compression_ratio: Optional[float]
    error: Optional[str] = None


class BatchSummarizeRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to summarize")
    max_length: int = Field(150, ge=30, le=500)
    min_length: int = Field(30, ge=10, le=200)


class ClusterRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to cluster", min_items=2)
    method: str = Field("hdbscan", description="Clustering method: 'hdbscan' or 'kmeans'")
    n_clusters: Optional[int] = Field(None, description="Number of clusters (for kmeans)", ge=2)
    min_cluster_size: int = Field(5, description="Minimum cluster size (for hdbscan)", ge=2)


class ClusterResponse(BaseModel):
    success: bool
    clusters: List[dict]
    num_clusters: int
    error: Optional[str] = None


class SimilarityRequest(BaseModel):
    query_text: str = Field(..., description="Query text")
    corpus_texts: List[str] = Field(..., description="Corpus of texts to search")
    top_k: int = Field(5, description="Number of similar texts to return", ge=1, le=50)
    threshold: float = Field(0.5, description="Minimum similarity threshold", ge=0.0, le=1.0)


# Helper functions
def get_classification_pipeline():
    global classification_pipeline
    if classification_pipeline is None:
        logger.info("Initializing classification pipeline")
        classification_pipeline = ClassificationPipeline()
    return classification_pipeline


def get_summarization_pipeline():
    global summarization_pipeline
    if summarization_pipeline is None:
        logger.info("Initializing summarization pipeline")
        summarization_pipeline = SummarizationPipeline()
    return summarization_pipeline


def get_clustering_pipeline():
    global clustering_pipeline
    if clustering_pipeline is None:
        logger.info("Initializing clustering pipeline")
        clustering_pipeline = ClusteringPipeline()
    return clustering_pipeline


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Service API",
        "version": "1.0.0",
        "endpoints": {
            "classify": "/api/classify",
            "batch_classify": "/api/classify/batch",
            "summarize": "/api/summarize",
            "batch_summarize": "/api/summarize/batch",
            "cluster": "/api/cluster",
            "similarity": "/api/similarity"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/classify", response_model=ClassifyResponse)
async def classify_text(request: ClassifyRequest):
    """
    Classify a single text into categories
    """
    try:
        pipeline = get_classification_pipeline()
        result = pipeline.process(
            text=request.text,
            top_k=request.top_k,
            threshold=request.threshold
        )
        return ClassifyResponse(**result)
    except Exception as e:
        logger.error(f"Classification endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/classify/batch")
async def batch_classify_texts(request: BatchClassifyRequest):
    """
    Classify multiple texts
    """
    try:
        pipeline = get_classification_pipeline()
        results = pipeline.batch_process(
            texts=request.texts,
            top_k=request.top_k,
            threshold=request.threshold
        )
        statistics = pipeline.get_statistics(results)
        
        return {
            "results": results,
            "statistics": statistics
        }
    except Exception as e:
        logger.error(f"Batch classification endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    """
    Summarize a single text
    """
    try:
        pipeline = get_summarization_pipeline()
        result = pipeline.process(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        return SummarizeResponse(**result)
    except Exception as e:
        logger.error(f"Summarization endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/summarize/batch")
async def batch_summarize_texts(request: BatchSummarizeRequest):
    """
    Summarize multiple texts
    """
    try:
        pipeline = get_summarization_pipeline()
        results = pipeline.batch_process(
            texts=request.texts,
            max_length=request.max_length,
            min_length=request.min_length
        )
        statistics = pipeline.get_statistics(results)
        
        return {
            "results": results,
            "statistics": statistics
        }
    except Exception as e:
        logger.error(f"Batch summarization endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/cluster", response_model=ClusterResponse)
async def cluster_texts(request: ClusterRequest):
    """
    Cluster similar texts together
    """
    try:
        pipeline = get_clustering_pipeline()
        
        if request.method == "hdbscan":
            result = pipeline.cluster_hdbscan(
                texts=request.texts,
                min_cluster_size=request.min_cluster_size
            )
        elif request.method == "kmeans":
            if request.n_clusters is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="n_clusters is required for kmeans method"
                )
            result = pipeline.cluster_kmeans(
                texts=request.texts,
                n_clusters=request.n_clusters
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid clustering method. Use 'hdbscan' or 'kmeans'"
            )
        
        return ClusterResponse(
            success=True,
            clusters=result["clusters"],
            num_clusters=result["num_clusters"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Clustering endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/similarity")
async def find_similar_texts(request: SimilarityRequest):
    """
    Find similar texts to a query
    """
    try:
        pipeline = get_clustering_pipeline()
        results = pipeline.find_similar(
            query_text=request.query_text,
            corpus_texts=request.corpus_texts,
            top_k=request.top_k,
            threshold=request.threshold
        )
        
        return {
            "success": True,
            "query": request.query_text,
            "similar_texts": results,
            "num_results": len(results)
        }
    except Exception as e:
        logger.error(f"Similarity endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Run server
if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
