from fastapi import FastAPI
from .database import engine, Base
from .routes import reports, summaries
from .config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
from .routes import verification
app.include_router(verification.router, prefix="/verify", tags=["verification"])
from .routes import news
app.include_router(news.router, prefix="/news", tags=["news"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Disaster Information Summarization Platform API"}
