from openai import OpenAI
import json
import requests

client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")

def call_mcp(arguments):
    """Send tool request to MCP"""
    response = requests.post("http://127.0.0.1:8000/tool_call", json=arguments)
    return response.json()

tools = [{
    "type": "function",
    "function": {
        "name": "query_database",
        "description": "Run an SQL query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "SQL query"},
                "db_name": {"type": "string", "description": "Database name"}
            },
            "required": ["query", "db_name"]
        }
    }
}]

response = client.chat.completions.create(
    model=client.models.list().data[0].id,
    messages=[{"role": "user", "content": "Show all records from climate_data"}],
    tools=tools,
    tool_choice="auto"
)

tool_call = response.choices[0].message.tool_calls[0].function
print(f"Function called: {tool_call.name}")
print(f"Arguments: {tool_call.arguments}")
print(f"Result: {call_mcp(json.loads(tool_call.arguments))}")

