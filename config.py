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

# Science fair test cases — see docs/experiment_design.md for rationale
TEST_CASES = [
    {"region_name": "Brazil",      "lat": -14.2,  "lon": -51.9, "country": "Brazil",      "disease": "dengue"},
    {"region_name": "Sudan",       "lat":  12.8,  "lon":  30.2, "country": "Sudan",       "disease": "cholera"},
    {"region_name": "Kenya",       "lat":  -0.02, "lon":  37.9, "country": "Kenya",       "disease": "malaria"},
    {"region_name": "Bangladesh",  "lat":  23.7,  "lon":  90.4, "country": "Bangladesh",  "disease": "dengue"},
    {"region_name": "Mozambique",  "lat": -18.7,  "lon":  35.5, "country": "Mozambique",  "disease": "cholera"},
]
