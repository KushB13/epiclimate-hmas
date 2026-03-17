# agents/disease_tracker_agent.py
# Reference: docs/architecture.md (Agent 4 contract)
# Reference: docs/api_reference.md (Gemini section)

from utils import call_gemini, parse_json_response


class DiseaseTrackerAgent:

    def run(self, country: str, disease: str) -> dict:
        """
        Fetches historical disease risk profile using Gemini.
        Returns: {disease, country, historical_risk_level, seasonal_peak_months, recent_trend, avg_annual_cases_estimate, key_risk_factors}
        """
        print(f"  [DiseaseTrackerAgent] {disease} in {country}...")

        fallback = {
            "disease": disease, "country": country,
            "historical_risk_level": "medium",
            "seasonal_peak_months": ["Unknown"],
            "recent_trend": "stable",
            "avg_annual_cases_estimate": "unknown",
            "key_risk_factors": ["climate sensitivity", "limited surveillance data"]
        }

        prompt = f"""You are a WHO epidemiologist with global disease surveillance knowledge.

Provide the historical outbreak risk profile for {disease} in {country}.
Base your answer on real WHO surveillance data and peer-reviewed research.

Return ONLY a JSON object with no other text, no markdown:
{{
  "disease": "{disease}",
  "country": "{country}",
  "historical_risk_level": "low|medium|high",
  "seasonal_peak_months": ["Month1", "Month2"],
  "recent_trend": "increasing|stable|decreasing",
  "avg_annual_cases_estimate": "e.g. 50000-100000",
  "key_risk_factors": ["factor1", "factor2", "factor3"]
}}
"""
        response_text = call_gemini(prompt)
        result = parse_json_response(response_text, fallback)
        
        print(f"  [DiseaseTrackerAgent] Done: {result.get('historical_risk_level')}")
        return result
