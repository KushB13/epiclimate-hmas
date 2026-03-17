# EpiClimate HMAS — API Reference

## Golden Rule
Never call APIs directly in agents.
Always use utils.safe_api_call() for HTTP.
Always use utils.call_gemini() for Gemini.

═══════════════════════════════════════
1. Open-Meteo Current Weather API
═══════════════════════════════════════
Base URL: https://api.open-meteo.com/v1/forecast
Method: GET
Auth: None required (free, no key)

Parameters for TemperatureAgent:
  latitude   float   e.g. -14.2
  longitude  float   e.g. -51.9
  current    string  "temperature_2m"

Parameters for PrecipitationAgent:
  latitude   float
  longitude  float
  current    string  "precipitation,relative_humidity_2m"

Response shape:
  {
    "current": {
      "temperature_2m": 31.2,
      "relative_humidity_2m": 78,
      "precipitation": 5.4
    }
  }

Access pattern:
  temp     = data["current"]["temperature_2m"]
  humidity = data["current"]["relative_humidity_2m"]
  precip   = data["current"]["precipitation"]

═══════════════════════════════════════
2. Open-Meteo Historical Archive API
═══════════════════════════════════════
Base URL: https://archive-api.open-meteo.com/v1/archive
Method: GET
Auth: None required

Parameters for TemperatureAgent:
  latitude    float
  longitude   float
  daily       string  "temperature_2m_mean"
  start_date  string  YYYY-MM-DD
  end_date    string  YYYY-MM-DD

Parameters for PrecipitationAgent:
  latitude    float
  longitude   float
  daily       string  "precipitation_sum"
  start_date  string  YYYY-MM-DD
  end_date    string  YYYY-MM-DD

Date calculation — always use this exact pattern:
  from datetime import datetime, timedelta
  end_date   = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
  start_date = (datetime.now() - timedelta(days=HISTORICAL_DAYS + 7)).strftime("%Y-%m-%d")

Response shape:
  {
    "daily": {
      "temperature_2m_mean": [26.1, 26.8, 27.2, ...],
      "precipitation_sum":   [2.1,  0.0,  5.3,  ...]
    }
  }

Historical average calculation:
  values = data["daily"].get("temperature_2m_mean", [])
  values = [v for v in values if v is not None]
  avg = round(sum(values) / len(values), 2) if values else 25.0

═══════════════════════════════════════
3. Google Gemini 2.0 Flash
═══════════════════════════════════════
Model:  gemini-2.0-flash
Auth:   GEMINI_API_KEY in .env file
SDK:    google-genai

Always call via utils — never directly:
  from utils import call_gemini, parse_json_response
  response_text = call_gemini(prompt)
  result = parse_json_response(response_text, fallback_dict)

JSON prompt rule — always end Gemini prompts with:
  "Return ONLY a JSON object with no other text, no markdown, no explanation."

Rate limits (free tier):
  15 requests per minute
  If 429 error: utils.call_gemini() waits 60s and retries once automatically
  After 1 retry: returns "" — agent uses fallback

═══════════════════════════════════════
4. SQLite (epiclimate.db)
═══════════════════════════════════════
Built into Python — no install needed.
Never import sqlite3 directly in agents or orchestrators.
Only use these functions from database.py:

  from database import init_db, save_prediction, get_all_predictions
  init_db()                    call once at startup in main.py
  save_prediction(full_report) call after each complete pipeline run
  rows = get_all_predictions() call to read all saved results
