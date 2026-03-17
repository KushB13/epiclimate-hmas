import os
import sys

# Ensure the root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)


from utils import call_gemini, parse_json_response

class AnomalyDetectorAgent:

    def run(self, region_name: str, temp_anomaly: float, precip_anomaly: float, humidity: float) -> dict:
        """
        Classifies climate anomaly risk using Gemini.
        Returns: {"anomaly_level": str, "reasoning": str}
        """
        print(f"  [AnomalyDetectorAgent] {region_name}...")

        fallback = {"anomaly_level": "MEDIUM", "reasoning": "Unable to assess — using moderate default"}

        prompt = f"""You are a climate scientist analyzing disease transmission risk.

Climate data for {region_name}:
- Temperature anomaly: {temp_anomaly}°C above or below the 90-day average
- Precipitation anomaly: {precip_anomaly}mm above or below the 90-day average
- Current humidity: {humidity}%

Classify the climate anomaly risk for disease transmission as:
LOW, MEDIUM, HIGH, or CRITICAL

Criteria:
- LOW: minimal deviation, low vector breeding risk
- MEDIUM: moderate anomaly, some elevated risk
- HIGH: significant anomaly, high breeding or waterborne risk
- CRITICAL: extreme anomaly, emergency-level risk

Return ONLY a JSON object with no other text, no markdown:
{{"anomaly_level": "LOW|MEDIUM|HIGH|CRITICAL", "reasoning": "2-3 sentence explanation"}}
"""
        response_text = call_gemini(prompt)
        result = parse_json_response(response_text, fallback)
        
        print(f"  [AnomalyDetectorAgent] Done: {result.get('anomaly_level')}")
        return result


