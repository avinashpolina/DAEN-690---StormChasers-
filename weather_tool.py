from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import logging
import re
from utils import extract_allowed_columns

app = FastAPI()
logging.basicConfig(level=logging.INFO)

DB_PATH = "regional_weather.db"
TABLE_NAME = "weather_data"

# Dynamically extract allowed columns
ALLOWED_COLUMNS = extract_allowed_columns(DB_PATH, TABLE_NAME)

# Synonyms for natural queries (will be remapped before validation)
COLUMN_SYNONYMS = {
    "temperature": "temp",
    "tempmax": "tempmax",
    "maximum temperature": "tempmax",
    "tempmin": "tempmin",
    "minimum temperature": "tempmin",
    "humidity": "humidity",
    "precipitation": "precip",
    "rainfall": "precip",
    "date": "datetime",
    "state": "state",
    "location": "state"
}

class SQLRequest(BaseModel):
    query: str

@app.post("/query")
def query_weather(request: SQLRequest):
    sql = request.query
    logging.info(f"Received SQL query: {sql}")

    # Remap synonyms for flexibility
    sql = remap_columns(sql, COLUMN_SYNONYMS)
    logging.info(f"Remapped SQL: {sql}")

    # Validate allowed tokens
    invalid = get_invalid_tokens(sql, ALLOWED_COLUMNS,TABLE_NAME)
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
    for k, v in mapping.items():
        pattern = re.compile(rf"\b{k}\b", re.IGNORECASE)
        sql = pattern.sub(v, sql)
    return sql

def get_invalid_tokens(sql: str, allowed_columns: set,table_name: str = "") -> list:
    invalid = []
    stripped_sql = re.sub(r"'[^']*'", "", sql.lower())
    tokens = stripped_sql.replace(",", " ").replace("(", " ").replace(")", " ").split()

    allowed_tokens = {"select", "from", "where", "and", "or", "*", "=", "limit", "like"}
    allowed_tokens.add(table_name.lower())  

    for token in tokens:
        token = token.strip("\"'")
        if token in allowed_tokens:
            continue
        if token in allowed_columns:
            continue
        if token.isnumeric():
            continue
        if any(col in token for col in allowed_columns):
            continue
        invalid.append(token)
    return invalid

