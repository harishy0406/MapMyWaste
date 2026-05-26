import sqlite3

con = sqlite3.connect('mapmywaste.db')
cur = con.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cur.fetchall()]
print('Tables:', tables)

if tables:
    for table in tables:
        cur.execute(f"PRAGMA table_info({table});")
        cols = [r[1] for r in cur.fetchall()]
        print(f"  {table}: {cols}")

con.close()
