from fastapi import FastAPI
from pydantic import BaseModel
import requests
import logging
import sqlite3
import json
from datetime import datetime

from tool_schemas import TOOL_SCHEMAS as tool_schemas

app = FastAPI()
logging.basicConfig(level=logging.INFO)

CLIMATEGPT_API_URL = "https://erasmus.ai/models/climategpt_8b_latest/v1/chat/completions"
AUTH = ("ai", "4climate")

TOOLS = {}

class QueryRequest(BaseModel):
    user_input: str

@app.post("/register")
def register_tool(name: str, api_url: str, description: str):
    TOOLS[name] = {"api_url": api_url, "description": description}
    logging.info(f"Tool '{name}' registered at {api_url}")
    return {"message": f"Tool '{name}' registered successfully", "tools": TOOLS}

@app.get("/list_tools")
def list_tools():
    return {"registered_tools": TOOLS}

@app.post("/query")
def query_mcp(request: QueryRequest):
    user_input = request.user_input
    logging.info(f"Received query: {user_input}")

    # Build prompt for ClimateGPT
    system_prompt = {
        "model": "/cache/climategpt_8b_latest",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a router system that decides which tool to use and generates an exact SQL query for that tool.\n\n"
                    "Rules:\n"
                    "- Use two-letter U.S. state codes for 'state' (e.g., CA, TX, NY).\n"
                    "- Match dates exactly (e.g., date = 'YYYY-MM-DD'); DO NOT use wildcards like LIKE or %.\n"
                    "- Do not include table names unless required.\n"
                    "- Do not wrap responses in code blocks.\n\n"
                    "Respond in this format:\n"
                    "{\n  \"tool\": \"tool_name\",\n  \"sql\": \"SELECT ...\"\n}\n\n"
                    "Tool schemas:\n"
                    "- weather_tool → table: `weather_data`, columns: ['datetime', 'state', 'temp', 'tempmin', 'tempmax', 'humidity', 'precip']\n"
                    "- emissions_tool → table: `emissions_data`, columns: ['date', 'country', 'sector', 'emissions']\n"
                    "- climate_financing_tool → table: `climate_financing`, columns: ['project_id', 'country', 'region', 'sector', 'funding_amount', 'year']\n"
                    "- air_quality_tool → table: `air_quality`, columns: ['date', 'state', 'o3', 'co', 'no2', 'so2', 'pm25', 'pm10']\n"
                    "- sector_emissions_tool → table: `sector_emissions`, columns: ['iso3_country', 'sector', 'subsector', 'start_time', 'end_time', 'lat', 'lon', 'gas', 'emissions_quantity', 'temporal_granularity', 'activity', 'activity_units', 'emissions_factor', 'emissions_factor_units', 'capacity', 'capacity_units', 'capacity_factor']\n"
                )
            },
            {
                "role": "user",
                "content": f"User query: {user_input}. Available tools: {list(TOOLS.keys())}"
            }
        ]
    }

    try:
        response = requests.post(CLIMATEGPT_API_URL, json=system_prompt, auth=AUTH)
        response.raise_for_status()
        raw = response.json()
        logging.info(f"ClimateGPT Raw: {json.dumps(raw, indent=2)}")
    except Exception as e:
        logging.error(f"LLM call failed: {str(e)}")
        return {"error": "LLM classification failed"}

    if "usage" in raw:
        logging.info(f"LLM Token Usage: {raw['usage']}")

    tool_name, sql_query = extract_tool_and_sql(raw)

    if not tool_name or not sql_query:
        logging.warning("No valid tool or SQL found in LLM response. Using fallback.")
        return {"response": fallback_llm_response(user_input)}

    logging.info(f"Tool selected: {tool_name}")
    logging.info(f"SQL generated: {sql_query}")

    if tool_name not in TOOLS:
        logging.warning(f"Tool '{tool_name}' is not registered.")
        return {"response": fallback_llm_response(user_input)}

    try:
        tool_api = TOOLS[tool_name]["api_url"]
        response = requests.post(tool_api, json={"query": sql_query})
        response.raise_for_status()
        result = response.json()
        logging.info(f"Tool result: {result}")
    except Exception as e:
        logging.error(f"Tool call failed: {str(e)}")
        return {"error": f"Tool call failed: {str(e)}"}

    log_query(user_input, tool_name, sql_query, result)
    return {"response": format_response_with_llm(user_input, result)}

def extract_tool_and_sql(raw_response: dict) -> tuple[str, str]:
    try:
        message = raw_response["choices"][0]["message"]
        content = message.get("content", "")
        parsed = json.loads(content)
        return parsed.get("tool"), parsed.get("sql")
    except Exception as e:
        logging.warning(f"Tool+SQL extraction failed: {str(e)}")
        return None, None

def fallback_llm_response(user_input: str) -> str:
    logging.info("Falling back to general LLM answer...")
    prompt = {
        "model": "/cache/climategpt_8b_latest",
        "messages": [
            {"role": "system", "content": "You are a helpful climate assistant."},
            {"role": "user", "content": user_input}
        ]
    }
    try:
        response = requests.post(CLIMATEGPT_API_URL, json=prompt, auth=AUTH)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logging.warning(f"General LLM fallback failed: {str(e)}")
        return "Sorry, I couldn't understand that."

def format_response_with_llm(user_input: str, result: dict) -> str:
    prompt = {
        "model": "/cache/climategpt_8b_latest",
        "messages": [
            {"role": "system", "content": "Format this result as a natural language answer to the original question."},
            {"role": "user", "content": f"User asked: {user_input}. Tool result: {result}"}
        ]
    }
    try:
        response = requests.post(CLIMATEGPT_API_URL, json=prompt, auth=AUTH)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logging.warning(f"LLM formatting failed: {str(e)}")
        return str(result)

def log_query(user_input: str, tool: str, sql: str, result: dict):
    try:
        conn = sqlite3.connect("query_log.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO query_logs (timestamp, user_input, tool_used, tool_input, result)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                user_input,
                tool,
                sql,
                json.dumps(result)
            )
        )
        conn.commit()
        conn.close()
        logging.info("Query logged.")
    except Exception as e:
        logging.warning(f"Log failed: {str(e)}")

