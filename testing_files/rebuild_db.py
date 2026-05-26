#!/usr/bin/env python
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import WasteReport

app = create_app()

with app.app_context():
    # Get engine and create all tables explicitly
    engine = db.engine
    
    # Drop old table if exists for a fresh start
    from sqlalchemy import exc
    try:
        WasteReport.__table__.drop(engine)
        print("Dropped old waste_report table")
    except exc.NoSuchTableError:
        print("No old table to drop")
    
    # Now create it fresh
    WasteReport.__table__.create(engine)
    print("Created waste_report table")
    
    # Verify
    from sqlalchemy import inspect
    insp = inspect(engine)
    cols = {c['name'] for c in insp.get_columns('waste_report')}
    
    print(f"\nColumns in database:")
    for c in sorted(insp.get_columns('waste_report'), key=lambda x: x['name']):
        print(f"  {c['name']}")
    
    required = {'image_hash', 'waste_score', 'is_spam'}
    if required.issubset(cols):
        print(f"\n✓ SUCCESS! All required columns present")
    else:
        print(f"\n❌ Missing: {required - cols}")
