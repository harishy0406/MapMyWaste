#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, WasteReport

app = create_app()

with app.app_context():
    # Create all tables

    db.create_all()
    
    # Now check columns via SQLAlchemy
    from sqlalchemy import inspect
    insp = inspect(db.engine)
    cols = insp.get_columns('waste_report')
    print('Columns in waste_report:')
    for c in cols:
        print(f"  - {c['name']:20} {c['type']}")
    
    # Check if our new columns exist
    col_names = {c['name'] for c in cols}
    print(f"\nimage_hash exists: {'image_hash' in col_names}")
    print(f"waste_score exists: {'waste_score' in col_names}")
    print(f"is_spam exists: {'is_spam' in col_names}")
    
    # Try to insert a test record
    print("\nDatabase file:", os.path.abspath('mapmywaste.db'))
    print("File exists:", os.path.exists('mapmywaste.db'))
    if os.path.exists('mapmywaste.db'):
        print("File size:", os.path.getsize('mapmywaste.db'), "bytes")
