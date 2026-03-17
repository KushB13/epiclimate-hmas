# agents/prediction_agent.py
# Reference: docs/architecture.md (Agent 6 contract)
# Reference: docs/api_reference.md (Gemini section)

from utils import call_gemini, parse_json_response


class PredictionAgent:

    def run(self, region_name: str, disease: str, country: str, anomaly_level: str, 
            correlation_score: int, historical_risk_level: str, recent_trend: str) -> dict:
        """
        Generates outbreak risk forecast using Gemini.
        Returns: {risk_score, confidence, predicted_window, key_factors, comparison_to_baseline}
        """
        print(f"  [PredictionAgent] Generating forecast...")

        fallback = {
            "risk_score": 40, "confidence": "low",
            "predicted_window": "4-6 weeks",
            "key_factors": ["insufficient data for full assessment"],
            "comparison_to_baseline": "Unable to compare without complete data"
        }

        prompt = f"""You are a public health outbreak forecasting expert.

Inputs for {disease} in {region_name}, {country}:
- Climate anomaly level: {anomaly_level}
- Correlation score: {correlation_score}/100
- Historical risk: {historical_risk_level}
- Recent trend: {recent_trend}

Generate a probabilistic outbreak risk forecast for the next 8 weeks.
Score 0 = no elevated risk. Score 100 = near-certain outbreak.

Return ONLY a JSON object with no other text, no markdown:
{{
  "risk_score": <integer 0-100>,
  "confidence": "low|medium|high",
  "predicted_window": "e.g. 3-5 weeks from now",
  "key_factors": ["factor1", "factor2", "factor3"],
  "comparison_to_baseline": "one sentence vs normal seasonal risk"
}}
"""
        response_text = call_gemini(prompt)
        result = parse_json_response(response_text, fallback)
        
        print(f"  [PredictionAgent] Done: {result.get('risk_score')}/100")
        return result
