"""
Database Migration Script
Recreates the database with the new schema including all new fields
"""

import os
import sys

# Remove old database
db_path = "disaster_local.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✅ Removed old database: {db_path}")

# Import and create new schema
from backend.app.database import Base, engine
from backend.app.models.report import Report

print("📊 Creating new database schema...")
Base.metadata.create_all(bind=engine)
print("✅ Database created successfully with new schema!")

print("\n📋 New Report Model Fields:")
print("  - id")
print("  - title (NEW)")
print("  - text")
print("  - source_type")
print("  - source_identifier")
print("  - timestamp")
print("  - is_verified")
print("  - verification_status")
print("  - disaster_category")
print("  - location")
print("  - submitted_by (NEW)")
print("  - summary (NEW)")
print("  - confidence_score (NEW)")

print("\n🎉 Database migration complete!")
