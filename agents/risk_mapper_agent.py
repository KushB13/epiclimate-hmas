# agents/risk_mapper_agent.py
# Reference: docs/architecture.md (Agent 7 contract)
# Reference: docs/api_reference.md (Gemini section)

from utils import call_gemini, parse_json_response


class RiskMapperAgent:

    def run(self, country: str, disease: str, risk_score: int, lat: float, lon: float) -> dict:
        """
        Identifies high-risk zones using Gemini.
        Returns: {high_risk_zones, population_at_risk_estimate, vulnerability_factors, healthcare_capacity}
        """
        print(f"  [RiskMapperAgent] mapping {country}...")

        fallback = {
            "high_risk_zones": [f"Rural {country}", f"Coastal {country}", f"Urban slums in {country}"],
            "population_at_risk_estimate": "unknown",
            "vulnerability_factors": ["limited healthcare access", "climate exposure"],
            "healthcare_capacity": "limited"
        }

        prompt = f"""You are a geographic health risk analyst.

A {disease} outbreak risk score of {risk_score}/100 has been
predicted for {country} (centered near {lat}, {lon}).

Identify specific sub-regions, cities, or population groups most
vulnerable based on geography, population density, and healthcare access.

Return ONLY a JSON object with no other text, no markdown:
{{
  "high_risk_zones": ["zone1", "zone2", "zone3"],
  "population_at_risk_estimate": "e.g. 2-4 million people",
  "vulnerability_factors": ["factor1", "factor2", "factor3"],
  "healthcare_capacity": "limited|moderate|adequate"
}}
"""
        response_text = call_gemini(prompt)
        result = parse_json_response(response_text, fallback)
        
        print(f"  [RiskMapperAgent] Done.")
        return result
