import os
import sys
from datetime import datetime, timedelta

# Ensure the root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)


from utils import safe_api_call
from config import OPEN_METEO_CURRENT_URL, OPEN_METEO_ARCHIVE_URL, HISTORICAL_DAYS

class TemperatureAgent:

    def run(self, region_name: str, lat: float, lon: float) -> dict:
        """
        Fetches current temp and 90-day historical average for a region.
        Calculates temperature anomaly = current - historical_avg.
        Returns: {region, current_temp_c, historical_avg_temp_c, temp_anomaly_c}
        """
        print(f"  [TemperatureAgent] {region_name}...")

        fallback = {
            "region": region_name,
            "current_temp_c": 25.0,
            "historical_avg_temp_c": 25.0,
            "temp_anomaly_c": 0.0,
            "temp_error": "API unavailable — using defaults"
        }

        current_data = safe_api_call(OPEN_METEO_CURRENT_URL, {
            "latitude": lat, "longitude": lon,
            "current": "temperature_2m"
        })

        if not current_data or "current" not in current_data:
            print(f"  [TemperatureAgent] WARNING: no current data for {region_name}")
            return fallback

        current_temp = float(current_data["current"].get("temperature_2m", 25.0))

        end_date   = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=HISTORICAL_DAYS + 7)).strftime("%Y-%m-%d")

        archive_data = safe_api_call(OPEN_METEO_ARCHIVE_URL, {
            "latitude": lat, "longitude": lon,
            "daily": "temperature_2m_mean",
            "start_date": start_date, "end_date": end_date
        })

        if archive_data and "daily" in archive_data:
            temps = [t for t in archive_data["daily"].get("temperature_2m_mean", []) if t is not None]
            historical_avg = round(sum(temps) / len(temps), 2) if temps else 25.0
        else:
            print(f"  [TemperatureAgent] WARNING: no archive data — defaulting to 25°C")
            historical_avg = 25.0

        anomaly = round(current_temp - historical_avg, 2)
        print(f"  [TemperatureAgent] Done: {current_temp}°C (avg {historical_avg}°C, anomaly {anomaly:+.1f}°C)")

        return {
            "region": region_name,
            "current_temp_c": round(current_temp, 2),
            "historical_avg_temp_c": historical_avg,
            "temp_anomaly_c": anomaly
        }


