import os
import sys

# Ensure the root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)


from utils import call_gemini_with_search, parse_json_response

class PredictionAgent:

    def run(self, region_name: str, disease: str, country: str,
            anomaly_level: str, correlation_score: int,
            historical_risk_level: str, recent_trend: str) -> dict:

        print(f"  [PredictionAgent] Forecast: {disease} in {region_name}...")

        fallback = {
            "risk_score":              40,
            "confidence":              "low",
            "predicted_window":        "4-6 weeks",
            "key_factors":             ["insufficient data"],
            "comparison_to_baseline":  "Unable to compare",
            "real_world_advisories":   "none found",
            "is_real_data":            False
        }

        prompt = f"""You are a public health outbreak forecasting expert.

Search for: "{disease} {country} outbreak forecast risk advisory 2024 2025 WHO CDC"

Then generate a forecast using ALL of the following:

INPUT DATA:
  Region:            {region_name}, {country}
  Disease:           {disease}
  Climate anomaly:   {anomaly_level}
  Correlation score: {correlation_score}/100
  Historical risk:   {historical_risk_level}
  Recent trend:      {recent_trend}

Incorporate any real WHO, CDC, or ECDC warnings found in search results.
A risk score of 0 means no elevated risk. A score of 100 means near-certain outbreak.

Return ONLY a JSON object with no other text, no markdown:
{{
  "risk_score": <integer 0-100>,
  "confidence": "low|medium|high",
  "predicted_window": "e.g. 3-5 weeks from now",
  "key_factors": ["factor1", "factor2", "factor3"],
  "comparison_to_baseline": "one sentence vs normal seasonal risk",
  "real_world_advisories": "any real WHO/CDC/ECDC advisories found, or none found",
  "is_real_data": true
}}"""

        response_text, search_queries = call_gemini_with_search(prompt)
        result = parse_json_response(response_text, fallback)
        result["is_real_data"] = True

        print(f"  [PredictionAgent] Done: risk={result.get('risk_score')}/100, "
              f"confidence={result.get('confidence')}, window={result.get('predicted_window')}")
        return result


