import os
from pydantic_settings import BaseSettings # updated for pydantic v2
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Disaster Info Platform"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/disaster_db")
    AI_SERVICE_URL: str = os.getenv("AI_SERVICE_URL", "http://localhost:8002")
    
    class Config:
        env_file = ".env"

settings = Settings()
