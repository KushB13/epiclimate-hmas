import os
import sys

# Ensure the root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)


from utils import call_gemini_with_search, parse_json_response

class CorrelationAgent:

    def run(self, region_name: str, disease: str, country: str,
            anomaly_level: str, anomaly_reasoning: str,
            disease_profile: dict) -> dict:

        print(f"  [CorrelationAgent] {disease} in {region_name}...")

        fallback = {
            "correlation_score":    40,
            "scientific_reasoning": "Moderate correlation assumed — web search unavailable",
            "supporting_research":  [],
            "is_real_data":         False
        }

        historical_risk   = disease_profile.get("historical_risk_level", "medium")
        recent_trend      = disease_profile.get("recent_trend", "stable")
        key_risk_factors  = disease_profile.get("key_risk_factors", [])
        active_outbreak   = disease_profile.get("active_outbreak", False)
        alert_count       = disease_profile.get("recent_alert_count", 0)
        current_situation = disease_profile.get("current_situation_summary", "")

        prompt = f"""You are an epidemiologist calculating a climate-disease correlation score.

Search for: "{disease} {country} climate change outbreak risk research 2024 2025"

Then analyze all of the following together:

CLIMATE SITUATION in {region_name}:
  Anomaly level:    {anomaly_level}
  Reasoning:        {anomaly_reasoning}

REAL-WORLD DISEASE DATA for {disease} in {country}:
  Historical risk:  {historical_risk}
  Recent trend:     {recent_trend}
  Active outbreak:  {active_outbreak}
  Recent alerts:    {alert_count} alerts in surveillance systems
  Current status:   {current_situation}
  Key risk factors: {key_risk_factors}

Using the web search results AND the data above, calculate how strongly
this climate pattern correlates with elevated {disease} outbreak risk.

Return ONLY a JSON object with no other text, no markdown:
{{
  "correlation_score": <integer 0-100>,
  "scientific_reasoning": "2-3 sentences citing real research or current evidence found",
  "supporting_research": ["real source or finding 1", "real source or finding 2"],
  "is_real_data": true
}}"""

        response_text, search_queries = call_gemini_with_search(prompt)
        result = parse_json_response(response_text, fallback)

        if active_outbreak and isinstance(result.get("correlation_score"), int):
            result["correlation_score"]      = min(100, result["correlation_score"] + 15)
            result["active_outbreak_boost"]  = True

        result["is_real_data"] = True
        print(f"  [CorrelationAgent] Done: score={result.get('correlation_score')}/100")
        return result


