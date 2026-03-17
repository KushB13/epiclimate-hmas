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

═══════════════════════════════════════
5. WHO Disease Outbreak News RSS
═══════════════════════════════════════
URL:    https://www.who.int/feeds/entity/csr/don/en/rss.xml
Auth:   None required
Format: XML/RSS
Call:   data_fetcher.fetch_who_outbreaks(disease, country)
Returns: list of {title, link, description, pub_date, source}
Notes:  Official UN outbreak declarations, updated in real time

═══════════════════════════════════════
6. ProMED Early Warning RSS
═══════════════════════════════════════
URL:    https://promedmail.org/promed-rss/
Auth:   None required
Format: XML/RSS
Call:   data_fetcher.fetch_promed_alerts(disease, country)
Returns: list of {title, link, description, pub_date, source}
Notes:  Often 2-4 weeks ahead of official WHO declarations

═══════════════════════════════════════
7. ReliefWeb Disasters API
═══════════════════════════════════════
URL:    https://api.reliefweb.int/v1/disasters
Auth:   None required
Format: REST JSON
Call:   data_fetcher.fetch_reliefweb_outbreaks(country)
Returns: list of {name, countries, status, date_start, url, source}
Notes:  UN humanitarian platform, active disaster records

═══════════════════════════════════════
8. GDELT Document API
═══════════════════════════════════════
URL:    https://api.gdeltproject.org/api/v2/doc/doc
Auth:   None required
Format: REST JSON
Call:   data_fetcher.fetch_gdelt_news(query, max_items)
Returns: list of {title, url, domain, date, source}
Notes:  Monitors every news outlet on Earth in real time

═══════════════════════════════════════
9. Gemini Web Search Grounding
═══════════════════════════════════════
SDK:    google-genai with types.Tool(google_search=types.GoogleSearch())
Auth:   Same GEMINI_API_KEY — no extra setup needed
Call:   utils.call_gemini_with_search(prompt)
Returns: (response_text: str, search_queries: list)
Notes:  Gemini searches Google live during generation
        Falls back to call_gemini() automatically if search fails
        Used by: CorrelationAgent, PredictionAgent, AlertPublisherAgent
