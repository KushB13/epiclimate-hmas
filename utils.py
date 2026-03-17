# utils.py
# Reference: docs/architecture.md (Key Design Rules)
# Reference: docs/api_reference.md (Gemini section)

import json, time, requests
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_RETRY_WAIT_SECONDS

_client = None

def get_gemini_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def call_gemini(prompt: str, max_retries: int = 1) -> str:
    """
    Sends a prompt to Gemini. Returns response text or "" on failure.
    Retries once on rate limit then stops — quota protection.
    Reference: docs/api_reference.md (Gemini section)
    """
    client = get_gemini_client()
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            return response.text.strip()
        except Exception as e:
            err = str(e).lower()
            if "429" in err or "quota" in err or "rate" in err:
                if attempt < max_retries:
                    print(f"  [RATE LIMIT] Waiting {GEMINI_RETRY_WAIT_SECONDS}s...")
                    time.sleep(GEMINI_RETRY_WAIT_SECONDS)
                    continue
                print(f"  [ERROR] Rate limit — skipping call.")
                return ""
            elif "401" in err or "403" in err or "api key" in err:
                print(f"  [ERROR] Invalid API key — check .env file.")
                return ""
            else:
                print(f"  [ERROR] Gemini attempt {attempt+1} failed: {e}")
                return ""
    return ""


def call_gemini_with_search(prompt: str, max_retries: int = 1) -> tuple:
    """
    Sends a prompt to Gemini WITH live Google Search grounding enabled.
    Gemini automatically searches the web and uses real current results.

    Use for agents that need live real-world information:
      DiseaseTrackerAgent, CorrelationAgent, PredictionAgent, AlertPublisherAgent

    Returns: (response_text: str, search_queries: list)
    On failure: returns ("", []) — caller uses its fallback dict
    """
    from google.genai import types

    client = get_gemini_client()

    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )

            grounding_queries = []
            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, "grounding_metadata") and candidate.grounding_metadata:
                    meta = candidate.grounding_metadata
                    if hasattr(meta, "web_search_queries"):
                        grounding_queries = list(meta.web_search_queries or [])

            text = response.text.strip() if response.text else ""
            if grounding_queries:
                print(f"  [WebSearch] Queries used: {grounding_queries}")
            return (text, grounding_queries)

        except Exception as e:
            err = str(e).lower()
            if "429" in err or "quota" in err or "rate" in err:
                if attempt < max_retries:
                    print(f"  [RATE LIMIT] Waiting {GEMINI_RETRY_WAIT_SECONDS}s before retry...")
                    time.sleep(GEMINI_RETRY_WAIT_SECONDS)
                    continue
                print(f"  [ERROR] Rate limit on web search — falling back to standard call.")
                return (call_gemini(prompt, max_retries=0), [])
            elif "400" in err:
                print(f"  [WARN] Web search unavailable — falling back to standard call.")
                return (call_gemini(prompt, max_retries=0), [])
            else:
                print(f"  [ERROR] Web search call failed attempt {attempt + 1}: {e}")
                return ("", [])

    return ("", [])


def parse_json_response(text: str, fallback: dict) -> dict:
    """
    Parses JSON from Gemini response. Strips code fences. Returns fallback on failure.
    Never raises exceptions.
    Reference: docs/api_reference.md (Gemini section)
    """
    if not text or not text.strip():
        return fallback
    cleaned = text.replace("```json", "").replace("```", "").strip()
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        print(f"  [WARN] No JSON found in response — using fallback.")
        return fallback
    try:
        return json.loads(cleaned[start:end+1])
    except json.JSONDecodeError as e:
        print(f"  [WARN] JSON parse error ({e}) — using fallback.")
        return fallback


def safe_api_call(url: str, params: dict, timeout: int = 10) -> dict:
    """
    GET request to a REST API. Returns {} on any failure — never raises.
    Reference: docs/api_reference.md (Open-Meteo sections)
    """
    try:
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        print(f"  [WARN] Timeout ({timeout}s): {url}")
    except requests.exceptions.ConnectionError:
        print(f"  [WARN] No connection: {url}")
    except requests.exceptions.HTTPError as e:
        print(f"  [WARN] HTTP {e.response.status_code}: {url}")
    except Exception as e:
        print(f"  [WARN] API error: {e}")
    return {}


def print_section(title: str):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")


def print_result(label: str, value):
    print(f"  {label:<32} {value}")


def geocode_location(name: str) -> tuple:
    """
    Looks up lat/lon for a city/region name using Open-Meteo Geocoding.
    Returns (lat, lon, country_name) or (None, None, None) on failure.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    res = safe_api_call(url, {"name": name, "count": 1, "language": "en", "format": "json"})
    results = res.get("results", [])
    if results:
        r = results[0]
        return r.get("latitude"), r.get("longitude"), r.get("country", "")
    return None, None, None
