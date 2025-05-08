from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import logging
import re
from utils import extract_allowed_columns

app = FastAPI()
logging.basicConfig(level=logging.INFO)

DB_PATH = "emissions.db"
TABLE_NAME = "emissions_data"

# Dynamically extract allowed columns
ALLOWED_COLUMNS = extract_allowed_columns(DB_PATH, TABLE_NAME)

# Synonyms for user-friendly queries
COLUMN_SYNONYMS = {
    "carbon emissions": "emissions",
    "co2": "emissions",
    "emission": "emissions",
    "carbon": "emissions",
    "country": "country",
    "nation": "country",
    "date": "date",
    "year": "date",
    "sector": "sector",
    "industry": "sector"
}

class SQLRequest(BaseModel):
    query: str

@app.post("/query")
def query_emissions(request: SQLRequest):
    sql = request.query
    logging.info(f"Received SQL query: {sql}")

    # Remap synonyms to standard column names
    sql = remap_columns(sql, COLUMN_SYNONYMS)
    logging.info(f"Remapped SQL: {sql}")

    # Validate column names
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
        logging.error(f" Query execution failed: {str(e)}")
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

