"""
Setup script to add ai_service to Python path
This allows importing ai_service modules from anywhere
"""
import sys
from pathlib import Path

# Add parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

print(f"Added {parent_dir} to Python path")
print("You can now import ai_service modules")
