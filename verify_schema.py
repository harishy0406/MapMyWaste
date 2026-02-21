import sqlite3

con = sqlite3.connect('mapmywaste.db')
cur = con.cursor()
cur.execute("PRAGMA table_info(waste_report);")
rows = cur.fetchall()

print('Columns in waste_report table:')
for i, (cid, name, typ, notnull, dflt_value, pk) in enumerate(rows, 1):
    print(f"  {i}. {name:20} - {typ}")

con.close()
