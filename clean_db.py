import sqlite3

conn = sqlite3.connect("patient_queries.db")
cursor = conn.cursor()

# Delete all entries except IDs 15 and 16
cursor.execute("DELETE FROM queries WHERE id NOT IN (15, 16)")
conn.commit()

# Verify remaining entries
cursor.execute("SELECT * FROM queries")
print("Remaining entries:", cursor.fetchall())

conn.close()