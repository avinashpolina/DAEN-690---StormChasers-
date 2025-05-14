# Storm Chasers – ClimateGPT (DAEN-690 Capstone Project)

Storm Chasers – ClimateGPT is a full-stack climate intelligence system developed as part of the DAEN-690 Capstone project at George Mason University. The system enables users to ask questions related to air quality, emissions, weather patterns, and climate finance using a client-hosted Large Language Model (LLM) via Erasmus.ai. It includes a React-based frontend, a modular Python backend with tool registration, and several climate-related datasets in CSV and database formats. The system also includes Docker support for containerized deployment.

## Project Objectives

- Provide an AI-powered assistant to answer complex climate-related questions
- Integrate environmental datasets into a tool-based architecture for querying
- Leverage Erasmus-hosted ClimateGPT for generating contextually rich answers
- Support deployment using Docker, Vercel (frontend), and Render (backend)

## Project Directory Structure

```
Daen_Final_StormChasers/
├── backend/                        # Optional Express proxy (if used)
│   └── server.js
├── dean_env/                      # Python virtual environment (should be ignored in version control)
├── csv_datasets/                  # Folder containing CSV/DB datasets
├── public/                        # React public folder
├── src/                           # React frontend source code
│   ├── App.js
│   ├── index.js
│   └── index.css
├── Dockerfile.air_quality         # Dockerfile for air quality tool
├── Dockerfile.climate_financing  # Dockerfile for climate finance tool
├── Dockerfile.emissions          # Dockerfile for emissions tool
├── Dockerfile.mcp                # Dockerfile for MCP server
├── Dockerfile.sector_emissions   # Dockerfile for sector emissions tool
├── Dockerfile.weather            # Dockerfile for weather tool
├── docker-compose.yml            # Compose file to spin up all services
├── ADB Climate Change Financing_merged.csv
├── AQI_cleaned.csv
├── Emissions_Dataset.csv
├── carbon_monitor_global.csv
├── emissions.db
├── adb_climate_financing.db
├── air_quality_index.db
├── sector_emissions.db
├── regional_weather.db
├── regional_data.csv
├── emissions_tool.py             # Tool to answer emissions-related queries
├── air_quality_tool.py           # Tool to answer air quality questions
├── weather_tool.py               # Tool to handle weather-based questions
├── climate_financing_tool.py     # Tool for climate finance data access
├── sector_emissions_tool.py      # Tool to analyze emissions by sector
├── llm_client.py                 # Module to connect to Erasmus ClimateGPT
├── mcp_server.py                 # Main backend routing controller
├── register_tool.py              # Registers all tool functions with the MCP
├── utils.py                      # Utility functions and logging
├── init_query_log.py             # Initializes query logging database
├── tool_schemas.py               # JSON schemas for tool input/output
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation (this file)
```
## Prerequisites

- Python 3.8 or higher
- pip
- Node.js and npm (for frontend)
- Git
- Vercel (for frontend deployment)
- Render (for backend deployment)

## Backend Setup (Python)

1. Create a virtual environment:
   python3 -m venv dean_env

2. Activate the environment:
   source dean_env/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Register all tools:
   python register_tool.py

5. Start the MCP server:
   python mcp_server.py

The MCP server will run on http://localhost:5000 and routes incoming LLM requests to the correct tool modules.

## Frontend Setup (React)

1. Navigate to the root of the frontend folder:
   cd Daen_Final_StormChasers

2. Install dependencies:
   npm install

3. Start the development server:
   npm start

Frontend will be available at http://localhost:3000. You can ask questions such as:
- "What is the AQI in Delhi?"
- "How much carbon was emitted globally in 2020?"
- "What is the weather pattern in region X?"
- "Which sector emits the most greenhouse gases?"

## API Integration – Erasmus.ai

The backend connects to the ClimateGPT API hosted at:
https://erasmus.ai/models/climategpt_8b_latest/v1/chat/completions

The API uses HTTP Basic Auth:
- Username: ai
- Password: 4climate

These credentials are securely encoded and sent via llm_client.py.

## Available Tools

- Emissions Tool: Analyzes and retrieves emissions data
- Air Quality Tool: Provides AQI details using air_quality_index.db
- Sector Emissions Tool: Breaks down emissions by economic sector
- Climate Finance Tool: Answers questions from climate finance datasets
- Weather Tool: Returns regional weather statistics
- MCP Server: Central server routing user questions to tools
- Erasmus LLM Client: Connects and formats data for ClimateGPT responses

## Database and CSV Files

| Filename                              | Type     | Description 
|---------------------------------------|----------|-------------------------------------
| AQI_cleaned.csv                       | CSV      | Air quality index data 
| Emissions_Dataset.csv                 | CSV      | Annual emissions data 
| carbon_monitor_global.csv             | CSV      | Global carbon monitoring 
| ADBClimateChange Financing_merged.csv | CSV      | Finance dataset from Asian Development Bank 
| regional_data.csv                     | CSV      | Region-level climate data 
| emissions.db                          | SQLite   | Emissions database 
| adb_climate_financing.db              | SQLite   | Finance data 
| sector_emissions.db                   | SQLite   | Emissions by sector 
| air_quality_index.db                  | SQLite   | AQI stored as a database 
| regional_weather.db                   | SQLite   | Regional weather data 
| query_log.db                          | SQLite   | Logging of queries sent to LLM 

## Docker Setup

If Docker is installed, you can spin up all services using:

docker-compose up --build

Each service has its own Dockerfile for modular development. Containers can be extended or scaled as needed.

## Deployment Instructions

### Frontend (Vercel)

1. Push your project to GitHub
2. Visit https://vercel.com and click "New Project"
3. Import the GitHub repo
4. Vercel auto-detects React → Deploy

### Backend (Render)

1. Create an account at https://render.com
2. Click "New Web Service"
3. Set root directory to your backend folder
4. Set start command: python mcp_server.py
5. Deploy and copy the backend URL
6. Update your React frontend to send API calls to the new backend URL

## Authors

Sai Avinash Polina 

Email: avinashpolina2028@gmail.com  

Bhuvan Sai Thatthari

Email: Bhu1work@gmail.com

Nimisha Menat

Email: nimishamenat@gmail.com

Akshitha Komatireddy

Email: akomati@gmu.edu

Sai Sahith Gabbeta 

Email: Saisahith650@gmail.com

Divya Atluri

Email: divyaatluri3@gmail.com

## License

This project is submitted as part of the DAEN-690 Capstone Project at George Mason University. It is intended for academic demonstration purposes only.
