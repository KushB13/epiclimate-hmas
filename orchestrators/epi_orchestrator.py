# orchestrators/epi_orchestrator.py
# Reference: docs/architecture.md (Tier 2B section)

from agents.disease_tracker_agent import DiseaseTrackerAgent
from agents.correlation_agent import CorrelationAgent
from agents.prediction_agent import PredictionAgent
from utils import print_section


class EpiOrchestrator:

    def __init__(self):
        self.disease_agent     = DiseaseTrackerAgent()
        self.correlation_agent = CorrelationAgent()
        self.prediction_agent  = PredictionAgent()

    def run(self, climate_report: dict, country: str, disease: str) -> dict:
        region_name = climate_report.get("region_name", country)
        print_section(f"SUB-ORCH 2B: Epi Intelligence — {disease} in {country}")

        fallback = {
            "country": country, "disease": disease,
            "risk_score": 40, "confidence": "low",
            "predicted_window": "4-6 weeks",
            "key_factors": ["pipeline error — fallback values"],
            "historical_risk_level": "medium", "recent_trend": "stable"
        }

        try:
            disease_result     = self.disease_agent.run(country, disease)
            correlation_result = self.correlation_agent.run(
                region_name=region_name, disease=disease, country=country,
                anomaly_level=climate_report.get("anomaly_level", "MEDIUM"),
                anomaly_reasoning=climate_report.get("reasoning", ""),
                disease_profile=disease_result
            )
            prediction_result  = self.prediction_agent.run(
                region_name=region_name, disease=disease, country=country,
                anomaly_level=climate_report.get("anomaly_level", "MEDIUM"),
                correlation_score=correlation_result.get("correlation_score", 40),
                historical_risk_level=disease_result.get("historical_risk_level", "medium"),
                recent_trend=disease_result.get("recent_trend", "stable")
            )

            report = {"country": country, "disease": disease,
                      **disease_result, **correlation_result, **prediction_result}

            print(f"  [EpiOrch] COMPLETE — Risk: {prediction_result.get('risk_score')}/100, "
                  f"Confidence: {prediction_result.get('confidence')}")
            return report

        except Exception as e:
            print(f"  [EpiOrch] ERROR: {e} — using fallback")
            return fallback
