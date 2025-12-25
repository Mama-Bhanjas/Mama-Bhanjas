import os
from pydantic_settings import BaseSettings # updated for pydantic v2
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Disaster Info Platform"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    AI_SERVICE_URL: str = os.getenv("AI_SERVICE_URL")
    
    class Config:
        env_file = ".env"

settings = Settings()
