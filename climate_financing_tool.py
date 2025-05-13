from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import logging
import re
from utils import extract_allowed_columns

# Initialize FastAPI application
app = FastAPI()
logging.basicConfig(level=logging.INFO)

DB_PATH = "adb_climate_financing.db"
TABLE_NAME = "climate_financing"  

# Dynamically extract allowed columns
ALLOWED_COLUMNS = extract_allowed_columns(DB_PATH, TABLE_NAME)


COLUMN_SYNONYMS = {
    "date": "Date_Signed",
    "signed date": "Date_Signed",
    "project": "Project_Name",
    "project name": "Project_Name",
    "project number": "Project_Number",
    "country": "Developing_Member_Country",
    "nation": "Developing_Member_Country",
    "country code": "Country_Code",
    "region": "Region",
    "department": "Department",
    "division": "Operations_Division",
    "category type": "Category_Type",
    "sector": "Sector",
    "primary sector": "Primary_Sector",
    "funding": "Project_Financing_Amount",
    "financing amount": "Project_Financing_Amount",
    "signed amount": "Signed_amount",
    "approval number": "Approval_number",
    "mode of assistance": "Mode_of_Financial_Assistance",
    "product": "Product_Type",
    "project type": "Project_Financing_Type",
    "fund source": "Fund_Source",
    "mitigation": "Mitigation_Finance",
    "adaptation": "Adaptation_Finance",
    "climate impact": "Climate_Change_Impact_on_the_Project",
    "response type": "Climate_Change_Response",
    "type of financing": "Type_of_Financing",
    "url": "Project_URL",
    "link": "Project_URL"
}

class SQLRequest(BaseModel):
    query: str

@app.post("/query")
def query_financing(request: SQLRequest):
    sql = request.query
    logging.info(f"Received SQL query: {sql}")

    # Remap synonyms to standard column names
    sql = remap_columns(sql, COLUMN_SYNONYMS)
    logging.info(f"Remapped SQL: {sql}")

    # Validate column names
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
    for k, v in mapping.items():
        pattern = re.compile(rf"\b{k}\b", re.IGNORECASE)
        sql = pattern.sub(v, sql)
    return sql

def get_invalid_tokens(sql: str, allowed_columns: set, table_name: str = "") -> list:
    invalid = []

    # Extract all backtick-quoted or unquoted potential column names
    quoted_columns = re.findall(r"`([^`]+)`", sql)
    stripped_sql = re.sub(r"`[^`]+`", "", sql)  # Remove quoted parts to avoid double counting

    # Also extract unquoted tokens
    tokens = stripped_sql.replace(",", " ").replace("(", " ").replace(")", " ").lower().split()

    # Standard allowed SQL syntax
    allowed_tokens = {"select", "from", "where", "and", "or", "*", "=", "like", "limit", "sum", "as"}
    allowed_tokens.add(table_name.lower())

    for token in tokens:
        token = token.strip("\"'")
        if token in allowed_tokens or token in allowed_columns or token.isnumeric():
            continue
        # If it partially matches an allowed column (e.g., "date" in "date_signed")
        if any(col.lower() in token for col in allowed_columns):
            continue
        invalid.append(token)

    # Also validate quoted column names directly
    for col in quoted_columns:
        if col not in allowed_columns:
            invalid.append(col)

    return invalid

