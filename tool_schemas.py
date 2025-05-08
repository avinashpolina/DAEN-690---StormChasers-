# tool_schemas.py

TOOL_SCHEMAS = {
    "weather_tool": {
        "table": "weather_data",
        "columns": [
            "state", "datetime", "temp", "tempmin", "tempmax", "humidity", "precip"
        ],
        "description": """
Tool for retrieving weather data across U.S. states. Data is collected per city per date.
- 'state': 2-letter abbreviation (e.g., 'CA', 'NY').
- 'datetime': full date in 'YYYY-MM-DD' format.
- 'temp', 'tempmin', 'tempmax': temperatures in Fahrenheit.
- 'humidity': percentage (0-100).
- 'precip': precipitation in inches.

Example rows:
1. CA, 2017-02-20, 58, 45, 63, 60, 0.12
2. NY, 2022-03-15, 50, 40, 58, 70, 0.25
3. TX, 2021-07-04, 85, 78, 91, 55, 0.05
""",
        "examples": [
            {
                "query": "What was the temperature in CA on 2017-02-20?",
                "sql": "SELECT temp FROM weather_data WHERE state = 'CA' AND datetime = '2017-02-20'"
            },
            {
                "query": "Show humidity in NY on 2022-03-15.",
                "sql": "SELECT humidity FROM weather_data WHERE state = 'NY' AND datetime = '2022-03-15'"
            },
            {
                "query": "Get precipitation in TX on 2021-07-04.",
                "sql": "SELECT precip FROM weather_data WHERE state = 'TX' AND datetime = '2021-07-04'"
            },
            {
                "query": "What were the minimum and maximum temperatures in CA on 2017-02-20?",
                "sql": "SELECT tempmin, tempmax FROM weather_data WHERE state = 'CA' AND datetime = '2017-02-20'"
            },
            {
                "query": "Get humidity for CA on 2017-02-20.",
                "sql": "SELECT humidity FROM weather_data WHERE state = 'CA' AND datetime = '2017-02-20'"
            }
        ]
    },

    "emissions_tool": {
        "table": "emissions_data",
        "columns": [
            "country", "date", "emissions"
        ],
        "description": """
Tool for retrieving national carbon emissions.
- 'country': full country name (e.g., 'United States', 'Canada').
- 'date': exact day in 'YYYY-MM-DD'.
- 'emissions': total emissions in metric tons (MtCO2).

Example rows:
1. United States, 2021-01-01, 3046318000
2. Canada, 2022-05-01, 850000000
3. Brazil, 2023-06-30, 720000000
""",
        "examples": [
            {
                "query": "What were the emissions in United States on 2021-01-01?",
                "sql": "SELECT emissions FROM emissions_data WHERE country = 'United States' AND date = '2021-01-01'"
            },
            {
                "query": "Get emissions in Canada on 2022-05-01.",
                "sql": "SELECT emissions FROM emissions_data WHERE country = 'Canada' AND date = '2022-05-01'"
            },
            {
                "query": "Emissions for Brazil on 2023-06-30?",
                "sql": "SELECT emissions FROM emissions_data WHERE country = 'Brazil' AND date = '2023-06-30'"
            },
            {
                "query": "How much did United States emit on 2021-01-01?",
                "sql": "SELECT emissions FROM emissions_data WHERE country = 'United States' AND date = '2021-01-01'"
            },
            {
                "query": "Show CO2 emissions of Canada on 2022-05-01.",
                "sql": "SELECT emissions FROM emissions_data WHERE country = 'Canada' AND date = '2022-05-01'"
            }
        ]
    },

    "climate_financing_tool": {
        "table": "climate_financing",
        "columns": [
            "Country_Code", "Developing_Member_Country", "Date_Signed",
            "Project_Name", "Signed_Amount", "Sector", "Primary_Sector", "Climate_Change_Response"
        ],
        "description": """
Tool for retrieving ADB climate financing project data.
- 'Country_Code': ISO 3-letter code (e.g., 'IND', 'PHL', 'USA').
- 'Developing_Member_Country': Full name (e.g., 'India').
- 'Date_Signed': format 'YYYY-MM-DD'.
- 'Project_Name': name of the funded project.
- 'Signed_Amount': amount signed (USD string).
- 'Sector', 'Primary_Sector': e.g., 'Energy', 'Transport'.
- 'Climate_Change_Response': e.g., 'Mitigation', 'Adaptation'.

Example rows:
1. IND, India, 2021-04-10, Solar Development Project, 1579000000, Energy, Renewable Energy, Mitigation
2. PHL, Philippines, 2020-06-15, Urban Climate Resilience, 830000000, Transport, Infrastructure, Adaptation
3. USA, United States, 2023-01-12, Smart Grid Expansion, 150000000, Energy, Grid Management, Mitigation
""",
        "examples": [
            {
                "query": "How much was signed for India projects in 2021?",
                "sql": "SELECT Signed_Amount FROM climate_financing WHERE Country_Code = 'IND' AND Date_Signed LIKE '2021%'"
            },
            {
                "query": "What projects were signed in Philippines in 2020?",
                "sql": "SELECT Project_Name FROM climate_financing WHERE Country_Code = 'PHL' AND Date_Signed LIKE '2020%'"
            },
            {
                "query": "Show sector for United States projects signed in 2023.",
                "sql": "SELECT Sector FROM climate_financing WHERE Country_Code = 'USA' AND Date_Signed LIKE '2023%'"
            },
            {
                "query": "Get climate response type for India projects.",
                "sql": "SELECT Climate_Change_Response FROM climate_financing WHERE Country_Code = 'IND'"
            },
            {
                "query": "List project names for Philippines in 2020.",
                "sql": "SELECT Project_Name FROM climate_financing WHERE Country_Code = 'PHL' AND Date_Signed LIKE '2020%'"
            }
        ]
    },

    "air_quality_tool": {
        "table": "air_quality",
        "columns": [
            "state", "county", "city", "date",
            "co_mean", "co_1st_max_value", "co_1st_max_hour", "co_aqi",
            "o3_mean", "o3_1st_max_value", "o3_1st_max_hour", "o3_aqi",
            "so2_mean", "so2_1st_max_value", "so2_1st_max_hour", "so2_aqi",
            "no2_mean", "no2_1st_max_value", "no2_1st_max_hour", "no2_aqi"
        ],
        "description": """
Tool for querying pollutant-based air quality data by location and date.
- 'state': full U.S. state name (e.g., 'California').
- 'city', 'county': exact names (case-sensitive).
- 'date': format 'YYYY-MM-DD'.

Pollutant columns:
- CO: co_mean, co_1st_max_value, co_1st_max_hour, co_aqi
- O3: o3_mean, o3_1st_max_value, o3_1st_max_hour, o3_aqi
- SO2: so2_mean, so2_1st_max_value, so2_1st_max_hour, so2_aqi
- NO2: no2_mean, no2_1st_max_value, no2_1st_max_hour, no2_aqi

Example rows:
1. California, Los Angeles, Los Angeles, 2023-07-10, 0.7, 1.2, 14, 30, 0.04, 0.08, 13, 45, 0.005, 0.01, 9, 5, 0.012, 0.025, 15, 18
2. Texas, Harris, Houston, 2023-06-15, 0.6, 1.1, 15, 28, 0.03, 0.07, 12, 40, 0.004, 0.009, 8, 4, 0.010, 0.021, 14, 16
3. New York, Queens, New York, 2023-05-20, 0.5, 0.9, 13, 25, 0.02, 0.06, 11, 35, 0.003, 0.007, 7, 3, 0.009, 0.018, 13, 14
""",
        "examples": [
            {
                "query": "Get carbon monoxide AQI in Los Angeles on 2023-07-10.",
                "sql": "SELECT co_aqi FROM air_quality WHERE city = 'Los Angeles' AND date = '2023-07-10'"
            },
            {
                "query": "Show ozone levels in Houston on 2023-06-15.",
                "sql": "SELECT o3_mean FROM air_quality WHERE city = 'Houston' AND date = '2023-06-15'"
            },
            {
                "query": "What was sulfur dioxide AQI in New York on 2023-05-20?",
                "sql": "SELECT so2_aqi FROM air_quality WHERE city = 'New York' AND date = '2023-05-20'"
            },
            {
                "query": "Get nitrogen dioxide mean in Queens on 2023-05-20.",
                "sql": "SELECT no2_mean FROM air_quality WHERE county = 'Queens' AND date = '2023-05-20'"
            },
            {
                "query": "Show carbon monoxide mean in Los Angeles on 2023-07-10.",
                "sql": "SELECT co_mean FROM air_quality WHERE city = 'Los Angeles' AND date = '2023-07-10'"
            }
        ]
    }
}


