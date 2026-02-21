#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

app = create_app()
print('Database URI:', app.config.get('SQLALCHEMY_DATABASE_URI'))
print('Database file path:', 'mapmywaste.db')
print('File exists before:', os.path.exists('mapmywaste.db'))

with app.app_context():
    # Try to get the engine and inspect it
    from sqlalchemy import inspect
    
    inspector = inspect(db.engine)
    print('Tables found:', inspector.get_table_names())
    
    # Try manual create
    print('\nCalling db.create_all()...')
    db.create_all()
    
    print('File exists after:', os.path.exists('mapmywaste.db'))
    print('File size:', os.path.getsize('mapmywaste.db') if os.path.exists('mapmywaste.db') else 'N/A')
    
    # Re-inspect
    inspector = inspect(db.engine)
    print('Tables found after create_all:', inspector.get_table_names())
