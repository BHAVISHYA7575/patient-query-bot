import sqlite3

# Connect to or create patient_queries.db
conn = sqlite3.connect("patient_queries.db")
cursor = conn.cursor()

# Create queries table (matching patient_query_bot.py structure)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        category TEXT
    )
""")

conn.commit()
conn.close()
print("Database and table created successfully.")