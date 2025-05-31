import sqlite3
conn = sqlite3.connect("patient_queries.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in database:", cursor.fetchall())
conn.close()