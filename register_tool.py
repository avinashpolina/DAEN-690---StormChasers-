import requests

mcp_url = "http://localhost:8000/register"

tools = [
    {
        "name": "weather_tool",  
        "api_url": "http://weather_tool:8001/query",
        "description": "Tool for retrieving temperature, humidity, and precipitation data across different U.S. states and dates."
    },
    {
        "name": "emissions_tool",  
        "api_url": "http://emissions_tool:8002/query",
        "description": "Tool for retrieving carbon emission levels by country and year."
    },
    {
        "name": "climate_financing_tool",
        "api_url": "http://climate_financing_tool:8003/query",
        "description": "Tool for analyzing ADB climate project funding by region, country, and sector."
    },
    {
        "name": "air_quality_tool",
        "api_url": "http://air_quality_tool:8004/query",
        "description": "Tool for querying air quality and pollutant AQI data across U.S. locations and dates."
    },
    {
    "name": "sector_emissions_tool",
    "api_url": "http://sector_emissions_tool:8005/query",
    "description": "Tool for querying emissions by country, sector, gas type, and capacity with temporal and spatial breakdowns."
    }
]

for tool in tools:
    response = requests.post(mcp_url, params=tool)
    print(response.json())

