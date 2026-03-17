# orchestrators/climate_orchestrator.py
# Reference: docs/architecture.md (Tier 2A section)

from agents.temperature_agent import TemperatureAgent
from agents.precipitation_agent import PrecipitationAgent
from agents.anomaly_detector_agent import AnomalyDetectorAgent
from utils import print_section


class ClimateOrchestrator:

    def __init__(self):
        self.temp_agent    = TemperatureAgent()
        self.precip_agent  = PrecipitationAgent()
        self.anomaly_agent = AnomalyDetectorAgent()

    def run(self, region_name: str, lat: float, lon: float) -> dict:
        print_section(f"SUB-ORCH 2A: Climate Intelligence — {region_name}")

        fallback = {
            "region_name": region_name, "lat": lat, "lon": lon,
            "anomaly_level": "MEDIUM", "reasoning": "Climate data unavailable",
            "temp_anomaly_c": 0.0, "precip_anomaly_mm": 0.0,
            "current_humidity_pct": 60.0
        }

        try:
            temp_result    = self.temp_agent.run(region_name, lat, lon)
            precip_result  = self.precip_agent.run(region_name, lat, lon)
            anomaly_result = self.anomaly_agent.run(
                region_name=region_name,
                temp_anomaly=temp_result.get("temp_anomaly_c", 0.0),
                precip_anomaly=precip_result.get("precip_anomaly_mm", 0.0),
                humidity=precip_result.get("current_humidity_pct", 60.0)
            )

            report = {"region_name": region_name, "lat": lat, "lon": lon,
                      **temp_result, **precip_result, **anomaly_result}

            print(f"  [ClimateOrch] COMPLETE — Anomaly: {anomaly_result.get('anomaly_level')}")
            return report

        except Exception as e:
            print(f"  [ClimateOrch] ERROR: {e} — using fallback")
            return fallback
