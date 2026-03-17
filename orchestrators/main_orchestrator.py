# orchestrators/main_orchestrator.py
# Reference: docs/architecture.md (Tier 1 and Data Flow sections)

import time
from orchestrators.climate_orchestrator import ClimateOrchestrator
from orchestrators.epi_orchestrator import EpiOrchestrator
from orchestrators.response_orchestrator import ResponseOrchestrator
from database import save_prediction
from utils import print_section, print_result
from config import PIPELINE_PAUSE_SECONDS


class MainOrchestrator:

    def __init__(self):
        self.climate_orch  = ClimateOrchestrator()
        self.epi_orch      = EpiOrchestrator()
        self.response_orch = ResponseOrchestrator()

    def run(self, region_name: str, lat: float, lon: float, 
            country: str, disease: str) -> dict:

        print_section(f"MAIN ORCHESTRATOR — {region_name} | {disease.upper()}")
        print(f"  Coordinates: ({lat}, {lon})")

        climate_report  = self.climate_orch.run(region_name, lat, lon)
        time.sleep(PIPELINE_PAUSE_SECONDS)

        epi_report      = self.epi_orch.run(climate_report, country, disease)
        time.sleep(PIPELINE_PAUSE_SECONDS)

        response_report = self.response_orch.run(climate_report, epi_report)

        full_report = {
            "region_name": region_name, "country": country,
            "disease": disease, "lat": lat, "lon": lon,
            **climate_report, **epi_report, **response_report
        }

        save_prediction(full_report)
        self._print_final_report(full_report)
        return full_report

    def _print_final_report(self, r: dict):
        print_section(f"FINAL REPORT — {r['region_name']} | {r['disease'].upper()}")
        print_result("Climate Anomaly Level:",  r.get("anomaly_level", "N/A"))
        print_result("Temperature Anomaly:",    f"{r.get('temp_anomaly_c', 0):+.1f}°C")
        print_result("Precipitation Anomaly:",  f"{r.get('precip_anomaly_mm', 0):+.1f}mm")
        print_result("Correlation Score:",      f"{r.get('correlation_score', 0)}/100")
        print_result("RISK SCORE:",             f"{r.get('risk_score', 0)}/100")
        print_result("Confidence:",             str(r.get("confidence","N/A")).upper())
        print_result("Predicted Window:",       r.get("predicted_window", "N/A"))
        print_result("Urgency Level:",          str(r.get("urgency_level","N/A")).upper())
        print(f"\n  HIGH-RISK ZONES:")
        for z in r.get("high_risk_zones", []):
            print(f"    - {z}")
        print(f"\n  TOP 3 ACTIONS:")
        for i, a in enumerate(r.get("recommended_actions", [])[:3], 1):
            print(f"    {i}. {a}")
        print(f"\n  BULLETIN:")
        words, line = r.get("alert_text", "No alert.").split(), "  "
        for w in words:
            if len(line) + len(w) > 62:
                print(line)
                line = "  " + w + " "
            else:
                line += w + " "
        if line.strip():
            print(line)
