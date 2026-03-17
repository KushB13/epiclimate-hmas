# agents/correlation_agent.py
# Reference: docs/architecture.md (Agent 5 contract)
# Reference: docs/api_reference.md (Gemini section)

from utils import call_gemini, parse_json_response


class CorrelationAgent:

    def run(self, region_name: str, disease: str, country: str, anomaly_level: str, 
            anomaly_reasoning: str, disease_profile: dict) -> dict:
        """
        Analyzes climate-disease correlations using Gemini.
        Returns: {"correlation_score": int, "scientific_reasoning": str}
        """
        print(f"  [CorrelationAgent] Analyzing {disease} correlation...")

        fallback = {"correlation_score": 40, "scientific_reasoning": "Moderate correlation — insufficient data for full assessment"}

        historical_risk_level = disease_profile.get("historical_risk_level", "medium")
        recent_trend = disease_profile.get("recent_trend", "stable")
        key_risk_factors = disease_profile.get("key_risk_factors", [])
        seasonal_peak_months = disease_profile.get("seasonal_peak_months", [])

        prompt = f"""You are an epidemiologist analyzing climate-disease correlations.

Climate situation in {region_name}:
- Anomaly level: {anomaly_level}
- Scientific reasoning: {anomaly_reasoning}

Disease profile for {disease} in {country}:
- Historical risk: {historical_risk_level}
- Recent trend: {recent_trend}
- Key risk factors: {key_risk_factors}
- Seasonal peaks: {seasonal_peak_months}

How strongly does this climate pattern correlate with elevated {disease}
outbreak risk based on established climate-disease research?

Return ONLY a JSON object with no other text, no markdown:
{{"correlation_score": <integer 0-100>, "scientific_reasoning": "2-3 sentence explanation"}}
"""
        response_text = call_gemini(prompt)
        result = parse_json_response(response_text, fallback)
        
        print(f"  [CorrelationAgent] Done: {result.get('correlation_score')}/100")
        return result
