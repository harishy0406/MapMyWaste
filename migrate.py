#!/usr/bin/env python
"""
Migration: Add image_hash, waste_score, is_spam columns to waste_report table
Run this once after updating models
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import WasteReport

app = create_app()
with app.app_context():
    # SQLAlchemy will create all tables if they don't exist 
    db.create_all()
    
    # Now add the columns if they don't already exist (for existing databases)
    import sqlite3
    db_path = 'mapmywaste.db'
    if os.path.exists(db_path):
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("PRAGMA table_info(waste_report);")
        cols = [r[1] for r in cur.fetchall()]
        
        changes = []
        if 'image_hash' not in cols:
            cur.execute("ALTER TABLE waste_report ADD COLUMN image_hash TEXT;")
            changes.append('image_hash')
        if 'waste_score' not in cols:
            cur.execute("ALTER TABLE waste_report ADD COLUMN waste_score REAL;")
            changes.append('waste_score')
        if 'is_spam' not in cols:
            cur.execute("ALTER TABLE waste_report ADD COLUMN is_spam INTEGER DEFAULT 0;")
            changes.append('is_spam')
        
        con.commit()
        con.close()
        
        if changes:
            print(f"✓ Migration successful! Added columns: {changes}")
        else:
            print("✓ All columns already exist")
    else:
        print("✓ Fresh database created with all columns")
