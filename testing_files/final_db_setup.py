#!/usr/bin/env python
import os
import sys

# Clear any existing module caches
if 'app' in sys.modules:
    del sys.modules['app']
if 'app.models' in sys.modules:
    del sys.modules['app.models']

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Force reimport
from app import create_app, db
# Explicit reimport of models
import importlib
import app.models
importlib.reload(app.models)
from app.models import WasteReport

app = create_app()

with app.app_context():
    # Print the model definition
    print("WasteReport columns from model definition:")
    for key, col in WasteReport.__table__.columns.items():
        print(f"  - {key:20} {col.type}")
    
    # Now create tables
    print("\nCreating database tables...")
    db.create_all()
    print("Done!")
    
    # Verify
    from sqlalchemy import inspect
    insp = inspect(db.engine)
    cols = insp.get_columns('waste_report')
    print('\nActual database columns:')
    for c in cols:
        print(f"  - {c['name']:20} {c['type']}")
