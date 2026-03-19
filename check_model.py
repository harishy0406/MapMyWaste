#!/usr/bin/env python
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Direct model import
from app.models import WasteReport

# Check the model definition itself
print("WasteReport table columns (from model __table__):")
for col in WasteReport.__table__.columns:
    print(f"  {col.name}")

# Show the expected columns
print("\nExpected columns from class definition:")
print("  image_hash, waste_score, is_spam") 