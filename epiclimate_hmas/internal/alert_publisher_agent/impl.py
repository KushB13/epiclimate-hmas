import os
import sys

# Ensure the root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)


from utils import call_gemini_with_search, call_gemini

class AlertPublisherAgent:

    def run(self, region_name: str, country: str, disease: str,
            risk_score: int, confidence: str, predicted_window: str,
            anomaly_level: str, key_factors: list,
            high_risk_zones: list, recommended_actions: list) -> dict:

        print(f"  [AlertPublisherAgent] Writing bulletin: {disease} in {region_name}...")

        fallback = {
            "alert_text": (
                f"EPICLIMATE ALERT — Elevated {disease} risk detected in {country}. "
                f"Risk score: {risk_score}/100. Confidence: {confidence}. "
                f"Predicted window: {predicted_window}. "
                "Public health authorities advised to review preparedness immediately."
            ),
            "is_real_data": False
        }

        top_3_actions = recommended_actions[:3] if recommended_actions else []

        prompt = f"""You are a WHO communications officer writing a public health bulletin.

Search for: "WHO {disease} {country} 2024 2025 outbreak bulletin advisory"

Use real current language and context from WHO/CDC if found in search results.

Then write a Disease Outbreak Risk Alert using:
  Location:      {region_name}, {country}
  Disease:       {disease}
  Risk Score:    {risk_score}/100
  Confidence:    {confidence}
  Time Window:   {predicted_window}
  Climate:       {anomaly_level} anomaly
  Key Factors:   {key_factors}
  Risk Areas:    {high_risk_zones}
  Top 3 Actions: {top_3_actions}

Style: WHO Disease Outbreak News tone. Factual. Plain English.
Reference any real current situation found in search results.
Begin with: "EPICLIMATE ALERT —"
Maximum 150 words. Plain text ONLY. No JSON. No markdown.
"""

        response_text, search_queries = call_gemini_with_search(prompt)

        if not response_text or len(response_text.strip()) < 20:
            response_text = call_gemini(
                prompt.replace(
                    f'Search for: "WHO {disease} {country} 2024 2025 outbreak bulletin advisory"\n\nUse real current language and context from WHO/CDC if found in search results.\n\nThen write',
                    "Write"
                )
            )

        alert_text = response_text.strip() if response_text else fallback["alert_text"]

        if not alert_text.startswith("EPICLIMATE ALERT"):
            alert_text = "EPICLIMATE ALERT — " + alert_text

        print(f"  [AlertPublisherAgent] Done: {len(alert_text)} chars")
        return {"alert_text": alert_text, "is_real_data": True}


