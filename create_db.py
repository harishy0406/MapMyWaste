#!/usr/bin/env python
"""Fresh database setup - no reload issues"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Start completely fresh
from app import create_app, db

app = create_app()
with app.app_context():
    # Create all tables - SQLAlchemy should pick up the updated model
    db.create_all()
    
    # Verify columns
    from sqlalchemy import inspect
    insp = inspect(db.engine)
    cols = {c['name'] for c in insp.get_columns('waste_report')}
    
    print('waste_report columns:')
    for c in insp.get_columns('waste_report'):
        print(f"  {c['name']}")
    
    missing = {'image_hash', 'waste_score', 'is_spam'} - cols
    if missing:
        print(f"\n❌ MISSING: {missing}")
        sys.exit(1)
    else:
        print(f"\n✓ All required columns present!")
