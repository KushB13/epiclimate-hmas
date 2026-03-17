# agents/alert_publisher_agent.py
# Reference: docs/architecture.md (Agent 9 contract)
# Reference: docs/api_reference.md (Gemini section)

from utils import call_gemini


class AlertPublisherAgent:

    def run(self, region_name: str, country: str, disease: str, risk_score: int, 
            confidence: str, predicted_window: str, anomaly_level: str, 
            key_factors: list, high_risk_zones: list, recommended_actions: list) -> dict:
        """
        Drafts a public health bulletin using Gemini.
        Returns: {"alert_text": str}
        """
        print(f"  [AlertPublisherAgent] drafting alert...")

        fallback = {
            "alert_text": f"EPICLIMATE ALERT — Elevated {disease} risk detected in {country}. "
                          f"Risk score: {risk_score}/100. Confidence: {confidence}. "
                          f"Predicted window: {predicted_window}. "
                          "Public health authorities advised to review preparedness immediately."
        }

        top_3_actions = recommended_actions[:3] if recommended_actions else ["Review preparedness"]

        prompt = f"""You are a WHO communications officer drafting a public health bulletin.

Write a Disease Outbreak Risk Alert for:
Location:     {region_name}, {country}
Disease:      {disease}
Risk Score:   {risk_score}/100
Confidence:   {confidence}
Time Window:  {predicted_window}
Anomaly:      {anomaly_level}
Key Factors:  {key_factors}
Risk Zones:   {high_risk_zones}
Top Actions:  {top_3_actions}

Style: WHO Disease Outbreak News tone. Plain English. Factual.
Begin with: "EPICLIMATE ALERT —"
Maximum 150 words. Plain text only. No JSON. No markdown.
"""
        response_text = call_gemini(prompt)
        
        if not response_text:
            return fallback

        print(f"  [AlertPublisherAgent] Done.")
        return {"alert_text": response_text.strip()}
