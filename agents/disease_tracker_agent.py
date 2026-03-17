# agents/disease_tracker_agent.py
"""
Disease Tracker Agent — Agent 4 of 9
Reference: docs/architecture.md (Agent 4 contract)
Reference: docs/api_reference.md (WHO RSS, ProMED, ReliefWeb, GDELT sections)

UPGRADED v1.1: Fetches REAL live outbreak data before asking Gemini.
Data flow:
  1. data_fetcher.fetch_all_outbreak_intelligence() pulls real alerts
  2. Real alerts injected into Gemini prompt as context
  3. Gemini analyzes real data, not guesses from training
"""

from utils import call_gemini, parse_json_response
from data_fetcher import fetch_all_outbreak_intelligence


class DiseaseTrackerAgent:

    def run(self, country: str, disease: str) -> dict:
        print(f"  [DiseaseTrackerAgent] {disease} in {country}...")

        fallback = {
            "disease":                   disease,
            "country":                   country,
            "historical_risk_level":     "medium",
            "seasonal_peak_months":      ["Unknown"],
            "recent_trend":              "stable",
            "avg_annual_cases_estimate": "unknown",
            "key_risk_factors":          ["climate sensitivity", "limited data"],
            "active_outbreak":           False,
            "recent_alert_count":        0,
            "current_situation_summary": "No real data retrieved",
            "is_real_data":              False,
            "data_sources":              []
        }

        # Step 1 — fetch real data from all sources
        real_data    = fetch_all_outbreak_intelligence(country, disease)
        sources_used = []

        # Step 2 — format real data as readable context for Gemini
        context_lines = []

        if real_data["who_alerts"]:
            context_lines.append(f"\nWHO DISEASE OUTBREAK NEWS ({len(real_data['who_alerts'])} alerts):")
            for a in real_data["who_alerts"][:3]:
                context_lines.append(f"  - {a['title']} ({a['pub_date'][:16]})")
            sources_used.append("WHO Disease Outbreak News")

        if real_data["promed_alerts"]:
            context_lines.append(f"\nPROMED EARLY WARNING ({len(real_data['promed_alerts'])} alerts):")
            for a in real_data["promed_alerts"][:3]:
                context_lines.append(f"  - {a['title']} ({a['pub_date'][:16]})")
            sources_used.append("ProMED")

        if real_data["reliefweb_events"]:
            context_lines.append(f"\nRELIEFWEB ACTIVE DISASTERS ({len(real_data['reliefweb_events'])} events):")
            for e in real_data["reliefweb_events"][:3]:
                context_lines.append(f"  - {e['name']} (Status: {e['status']}, Date: {e['date_start']})")
            sources_used.append("ReliefWeb")

        if real_data["news_articles"]:
            context_lines.append(f"\nRECENT NEWS ({len(real_data['news_articles'])} articles):")
            for n in real_data["news_articles"][:3]:
                context_lines.append(f"  - {n['title']} ({n['date'][:8]})")
            sources_used.append("GDELT Global News")

        real_context  = "\n".join(context_lines) if context_lines else "No real-time alerts found — use general knowledge."
        total_alerts  = (len(real_data["who_alerts"]) +
                         len(real_data["promed_alerts"]) +
                         len(real_data["reliefweb_events"]))
        active_outbreak = total_alerts > 0

        # Step 3 — build prompt with real data injected
        prompt = f"""You are a WHO epidemiologist analyzing real surveillance data.

REAL-TIME SURVEILLANCE DATA FOR {disease.upper()} IN {country.upper()}:
{real_context}

Using the real data above AND your epidemiological knowledge, produce a
risk profile for {disease} in {country}. If real alerts were found above,
prioritize them over general knowledge.

Return ONLY a JSON object with no other text, no markdown, no explanation:
{{
  "disease": "{disease}",
  "country": "{country}",
  "historical_risk_level": "low|medium|high",
  "seasonal_peak_months": ["Month1", "Month2"],
  "recent_trend": "increasing|stable|decreasing",
  "avg_annual_cases_estimate": "e.g. 50000-100000",
  "key_risk_factors": ["factor1", "factor2", "factor3"],
  "active_outbreak": {str(active_outbreak).lower()},
  "current_situation_summary": "1-2 sentence summary of current real-world situation"
}}"""

        response_text = call_gemini(prompt)
        result        = parse_json_response(response_text, fallback)

        # Step 4 — attach real data metadata
        result["recent_alert_count"] = total_alerts
        result["active_outbreak"]    = active_outbreak
        result["is_real_data"]       = True
        result["data_sources"]       = sources_used if sources_used else ["Gemini knowledge"]

        print(f"  [DiseaseTrackerAgent] Done: risk={result.get('historical_risk_level')}, "
              f"alerts={total_alerts}, active_outbreak={active_outbreak}")
        return result
