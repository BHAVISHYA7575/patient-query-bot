import sqlite3
conn = sqlite3.connect("patient_queries.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM queries")
print("Database entries:", cursor.fetchall())
conn.close()