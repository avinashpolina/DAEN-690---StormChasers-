import sqlite3

def extract_allowed_columns(db_path: str, table_name: str) -> set:
    """
    Returns a set of column names for a given table in a SQLite database.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = {row[1] for row in cursor.fetchall()}
        conn.close()
        return columns
    except Exception as e:
        print(f"Error extracting columns from {db_path}: {e}")
        return set()

