from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import logging
import re
from utils import extract_allowed_columns

app = FastAPI()
logging.basicConfig(level=logging.INFO)

DB_PATH = "sector_emissions.db"
TABLE_NAME = "sector_emissions"
ALLOWED_COLUMNS = extract_allowed_columns(DB_PATH, TABLE_NAME)

COLUMN_SYNONYMS = {
    "country": "iso3_country",
    "nation": "iso3_country",
    "gas type": "gas",
    "ghg": "gas",
    "emissions": "emissions_quantity",
    "emission quantity": "emissions_quantity",
    "quantity": "emissions_quantity",
    "sector": "sector",
    "sub-sector": "subsector",
    "sub sector": "subsector",
    "start time": "start_time",
    "end time": "end_time",
    "date range": "start_time",
    "location": "lat",
    "latitude": "lat",
    "longitude": "lon",
    "activity amount": "activity",
    "activity level": "activity",
    "activity units": "activity_units",
    "factor": "emissions_factor",
    "emissions factor": "emissions_factor",
    "emissions factor units": "emissions_factor_units",
    "capacity": "capacity",
    "capacity units": "capacity_units",
    "capacity factor": "capacity_factor"
}

class SQLRequest(BaseModel):
    query: str

@app.post("/query")
def query_sector_emissions(request: SQLRequest):
    sql = request.query
    logging.info(f"Received SQL query: {sql}")
    sql = remap_columns(sql, COLUMN_SYNONYMS)
    logging.info(f"Remapped SQL: {sql}")
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
    for k in sorted(mapping, key=len, reverse=True):
        pattern = re.compile(rf"\b{k}\b", re.IGNORECASE)
        sql = pattern.sub(mapping[k], sql)
    return sql

def get_invalid_tokens(sql: str, allowed_columns: set, table_name: str = "") -> list:
    invalid = []
    stripped_sql = re.sub(r"'[^']*'", "", sql.lower())
    quoted_columns = re.findall(r"`([^`]+)`", sql)
    tokens = re.split(r"[ ,()=]", stripped_sql)
    tokens = [t.strip("\"'`") for t in tokens if t.strip()]
    allowed_tokens = {
        "select", "from", "where", "and", "or", "*", "=", "limit", "like", "sum", "avg", "count", "min", "max", "as",
        "lower", "upper", "group", "by", "order", "asc", "desc"
    }
    allowed_tokens.add(table_name.lower())
    allowed_columns_lower = {col.lower() for col in allowed_columns}
    for token in tokens:
        if token in allowed_tokens or token in allowed_columns_lower:
            continue
        if any(col.lower() in token for col in allowed_columns):
            continue
        invalid.append(token)
    for col in quoted_columns:
        if col not in allowed_columns and col != table_name:
            invalid.append(col)
    return invalid

