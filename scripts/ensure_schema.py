import sqlite3, os
 
DB='mapmywaste.db'
if not os.path.exists(DB):
    print('DB not found, nothing to migrate:', DB)
    raise SystemExit(1)

con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute("PRAGMA table_info(waste_report);")
cols = [r[1] for r in cur.fetchall()]
print('Existing columns:', cols)
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
if changes:
    print('Added columns:', changes)
else:
    print('No changes needed')
con.close()
