from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import logging
import re
from utils import extract_allowed_columns

app = FastAPI()
logging.basicConfig(level=logging.INFO)

DB_PATH = "air_quality_index.db"
TABLE_NAME = "air_quality"

# Dynamically extract allowed columns
ALLOWED_COLUMNS = extract_allowed_columns(DB_PATH, TABLE_NAME)

# Synonyms for natural queries
COLUMN_SYNONYMS = {
    "ozone": "o3_aqi",
    "ozone aqi": "o3_aqi",
    "o3": "o3_aqi",
    "co": "co_aqi",
    "carbon monoxide": "co_aqi",
    "so2": "so2_aqi",
    "sulfur dioxide": "so2_aqi",
    "no2": "no2_aqi",
    "nitrogen dioxide": "no2_aqi",
    "state": "state",
    "county": "county",
    "city": "city",
    "location": "address",
    "date": "date"
}

class SQLRequest(BaseModel):
    query: str

@app.post("/query")
def query_air_quality(request: SQLRequest):
    sql = request.query
    logging.info(f"Received SQL query: {sql}")

    # Remap synonyms to real column names
    sql = remap_columns(sql, COLUMN_SYNONYMS)
    logging.info(f"Remapped SQL: {sql}")

    # Validate columns
    invalid = get_invalid_tokens(sql, ALLOWED_COLUMNS, TABLE_NAME)
    if invalid:
        logging.warning(f"Invalid tokens in SQL: {invalid}")
        return {"error": f"Unrecognized or disallowed columns: {sorted(invalid)}"}

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        logging.info(f"Query successful. Returned {len(result)} rows.")
        return {"result": result}
    except Exception as e:
        logging.error(f"Query execution failed: {str(e)}")
        return {"error": str(e)}


def remap_columns(sql: str, mapping: dict) -> str:
    for k in sorted(mapping, key=len, reverse=True):  # longest match first
        pattern = re.compile(rf"\b{k}\b", re.IGNORECASE)
        sql = pattern.sub(mapping[k], sql)
    return sql

def get_invalid_tokens(sql: str, allowed_columns: set, table_name: str = "") -> list:
    invalid = []

    # Remove string literals (e.g., 'arizona') to avoid false positives
    stripped_sql = re.sub(r"'[^']*'", "", sql.lower())

    # Extract quoted identifiers (e.g., `co_mean`)
    quoted_columns = re.findall(r"`([^`]+)`", sql)

    # Tokenize remaining SQL
    tokens = re.split(r"[ ,()=]", stripped_sql)
    tokens = [t.strip("\"'`") for t in tokens if t.strip()]

    # Allowable base tokens
    allowed_tokens = {
        "select", "from", "where", "and", "or", "*", "=", "limit", "like", "sum", "avg", "count", "min", "max", "as",
        "lower", "upper", "group", "by", "order", "asc", "desc"
    }
    allowed_tokens.add(table_name.lower())
    allowed_columns_lower = {col.lower() for col in allowed_columns}

    for token in tokens:
        if token in allowed_tokens:
            continue
        if token in allowed_columns_lower:
            continue
        if any(col.lower() in token for col in allowed_columns):
            continue
        invalid.append(token)

    # Also validate quoted columns and table names
    for col in quoted_columns:
        if col not in allowed_columns and col != table_name:
            invalid.append(col)

    return invalid

