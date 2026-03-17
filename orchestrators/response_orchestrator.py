# orchestrators/response_orchestrator.py
# Reference: docs/architecture.md (Tier 2C section)

from agents.risk_mapper_agent import RiskMapperAgent
from agents.resource_recommender_agent import ResourceRecommenderAgent
from agents.alert_publisher_agent import AlertPublisherAgent
from utils import print_section


class ResponseOrchestrator:

    def __init__(self):
        self.risk_mapper  = RiskMapperAgent()
        self.resource_rec = ResourceRecommenderAgent()
        self.alert_pub    = AlertPublisherAgent()

    def run(self, climate_report: dict, epi_report: dict) -> dict:
        region_name = climate_report.get("region_name", "Unknown")
        country     = epi_report.get("country", "Unknown")
        disease     = epi_report.get("disease", "Unknown")
        risk_score  = epi_report.get("risk_score", 40)
        print_section(f"SUB-ORCH 2C: Response Intelligence — {region_name}")

        fallback = {
            "high_risk_zones": [f"Rural {country}", f"Urban {country}"],
            "recommended_actions": ["Increase surveillance", "Pre-position supplies"],
            "urgency_level": "urgent",
            "alert_text": f"EPICLIMATE ALERT — Elevated {disease} risk in {country}. "
                          f"Risk score: {risk_score}/100. Authorities advised to prepare."
        }

        try:
            risk_result     = self.risk_mapper.run(
                country=country, disease=disease, risk_score=risk_score,
                lat=climate_report.get("lat", 0.0), lon=climate_report.get("lon", 0.0))

            resource_result = self.resource_rec.run(
                country=country, disease=disease, risk_score=risk_score,
                high_risk_zones=risk_result.get("high_risk_zones", []),
                healthcare_capacity=risk_result.get("healthcare_capacity", "limited"),
                predicted_window=epi_report.get("predicted_window", "4-6 weeks"))

            alert_result    = self.alert_pub.run(
                region_name=region_name, country=country, disease=disease,
                risk_score=risk_score,
                confidence=epi_report.get("confidence", "low"),
                predicted_window=epi_report.get("predicted_window", "4-6 weeks"),
                anomaly_level=climate_report.get("anomaly_level", "MEDIUM"),
                key_factors=epi_report.get("key_factors", []),
                high_risk_zones=risk_result.get("high_risk_zones", []),
                recommended_actions=resource_result.get("recommended_actions", []))

            report = {**risk_result, **resource_result, **alert_result}
            print(f"  [ResponseOrch] COMPLETE — Urgency: {resource_result.get('urgency_level')}")
            return report

        except Exception as e:
            print(f"  [ResponseOrch] ERROR: {e} — using fallback")
            return fallback
