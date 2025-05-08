import sqlite3
from datetime import datetime

conn = sqlite3.connect("query_log.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS query_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    user_input TEXT,
    tool_used TEXT,
    tool_input TEXT,
    result TEXT
)
""")

conn.commit()
conn.close()
print(" query_log.db created successfully.")

