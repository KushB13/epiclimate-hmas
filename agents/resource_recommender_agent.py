# agents/resource_recommender_agent.py
# Reference: docs/architecture.md (Agent 8 contract)
# Reference: docs/api_reference.md (Gemini section)

from utils import call_gemini, parse_json_response


class ResourceRecommenderAgent:

    def run(self, country: str, disease: str, risk_score: int, high_risk_zones: list, 
            healthcare_capacity: str, predicted_window: str) -> dict:
        """
        Recommends interventions using Gemini.
        Returns: {recommended_actions, urgency_level, lead_time_weeks, estimated_impact}
        """
        print(f"  [ResourceRecommenderAgent] generating recommendations...")

        fallback = {
            "recommended_actions": [
                f"Increase {disease} surveillance in high-risk zones of {country}",
                "Pre-position oral rehydration and treatment supplies",
                "Issue community health advisories in local languages",
                "Brief healthcare workers on outbreak recognition protocols",
                "Activate emergency response standby"
            ],
            "urgency_level": "urgent",
            "lead_time_weeks": 4,
            "estimated_impact": "Unable to estimate without full data"
        }

        prompt = f"""You are a WHO emergency preparedness coordinator.

Situation:
- Disease: {disease} in {country}
- Risk score: {risk_score}/100
- Predicted window: {predicted_window}
- High-risk zones: {high_risk_zones}
- Healthcare capacity: {healthcare_capacity}

Recommend 5 specific actionable interventions to initiate IMMEDIATELY
before the predicted outbreak window begins.

Return ONLY a JSON object with no other text, no markdown:
{{
  "recommended_actions": ["action1", "action2", "action3", "action4", "action5"],
  "urgency_level": "routine|urgent|emergency",
  "lead_time_weeks": <integer>,
  "estimated_impact": "brief statement on cases or lives preventable"
}}
"""
        response_text = call_gemini(prompt)
        result = parse_json_response(response_text, fallback)
        
        print(f"  [ResourceRecommenderAgent] Done.")
        return result
