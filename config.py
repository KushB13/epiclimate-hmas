# config.py
# Reference: docs/project_specs.md and docs/architecture.md

import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY             = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL               = "gemini-1.5-flash"
OPEN_METEO_CURRENT_URL     = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_ARCHIVE_URL     = "https://archive-api.open-meteo.com/v1/archive"
HISTORICAL_DAYS            = 90
RISK_LOW                   = 30
RISK_MEDIUM                = 60
RISK_HIGH                  = 80
GEMINI_RETRY_WAIT_SECONDS  = 60
PIPELINE_PAUSE_SECONDS     = 3

# Current test cases — uses live data for every run
TEST_CASES = [
    {"region_name": "Peru",         "lat": -9.19,  "lon": -75.01, "country": "Peru",         "disease": "dengue"},
    {"region_name": "Zambia",       "lat": -13.13, "lon":  27.85, "country": "Zambia",       "disease": "cholera"},
    {"region_name": "Pakistan",     "lat": 30.37,  "lon":  69.34, "country": "Pakistan",     "disease": "malaria"},
    {"region_name": "Philippines",  "lat": 12.87,  "lon": 121.77, "country": "Philippines",  "disease": "leptospirosis"},
    {"region_name": "Nigeria",      "lat":  9.08,  "lon":   8.67, "country": "Nigeria",      "disease": "lassa fever"},
]
