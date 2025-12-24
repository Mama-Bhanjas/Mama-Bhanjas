@echo off
REM Run the AI service test suite
cd /d "%~dp0"
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path.cwd().parent))" & python test_service.py
