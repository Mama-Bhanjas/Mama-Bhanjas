@echo off
REM Run the AI service API server
cd /d "%~dp0"
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
