# agents/precipitation_agent.py
# Reference: docs/architecture.md (Agent 2 contract)
# Reference: docs/api_reference.md (Open-Meteo Current + Archive sections)

from datetime import datetime, timedelta
from utils import safe_api_call
from config import OPEN_METEO_CURRENT_URL, OPEN_METEO_ARCHIVE_URL, HISTORICAL_DAYS


class PrecipitationAgent:

    def run(self, region_name: str, lat: float, lon: float) -> dict:
        """
        Fetches current precip, humidity and 90-day historical average precip for a region.
        Calculates precip anomaly = current - historical_avg.
        Returns: {region, current_precip_mm, historical_avg_precip_mm, precip_anomaly_mm, current_humidity_pct}
        """
        print(f"  [PrecipitationAgent] {region_name}...")

        fallback = {
            "region": region_name,
            "current_precip_mm": 0.0,
            "historical_avg_precip_mm": 0.0,
            "precip_anomaly_mm": 0.0,
            "current_humidity_pct": 60.0,
            "precip_error": "API unavailable — using defaults"
        }

        current_data = safe_api_call(OPEN_METEO_CURRENT_URL, {
            "latitude": lat, "longitude": lon,
            "current": "precipitation,relative_humidity_2m"
        })

        if not current_data or "current" not in current_data:
            print(f"  [PrecipitationAgent] WARNING: no current data for {region_name}")
            return fallback

        current_precip = float(current_data["current"].get("precipitation", 0.0))
        current_humidity = float(current_data["current"].get("relative_humidity_2m", 60.0))

        end_date   = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=HISTORICAL_DAYS + 7)).strftime("%Y-%m-%d")

        archive_data = safe_api_call(OPEN_METEO_ARCHIVE_URL, {
            "latitude": lat, "longitude": lon,
            "daily": "precipitation_sum",
            "start_date": start_date, "end_date": end_date
        })

        if archive_data and "daily" in archive_data:
            precips = [p for p in archive_data["daily"].get("precipitation_sum", []) if p is not None]
            historical_avg = round(sum(precips) / len(precips), 2) if precips else 0.0
        else:
            print(f"  [PrecipitationAgent] WARNING: no archive data — defaulting to 0.0mm")
            historical_avg = 0.0

        anomaly = round(current_precip - historical_avg, 2)
        print(f"  [PrecipitationAgent] Done: {current_precip}mm (avg {historical_avg}mm, anomaly {anomaly:+.1f}mm)")

        return {
            "region": region_name,
            "current_precip_mm": round(current_precip, 2),
            "historical_avg_precip_mm": historical_avg,
            "precip_anomaly_mm": anomaly,
            "current_humidity_pct": current_humidity
        }
