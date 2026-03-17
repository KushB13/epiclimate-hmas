# EpiClimate HMAS — System Architecture

## Overview
Two-tier Hierarchical Multi-Agent System.
Tier 1: Main Orchestrator (1 component)
Tier 2: Three Sub-Orchestrators, each coordinating 3 specialist agents
Total: 1 main + 3 sub-orchestrators + 9 agents = 13 active components

## Tier Map

TIER 1
MainOrchestrator
  Input:  region_name, lat, lon, country, disease
  Output: full_report dict
  Saves:  epiclimate.db

TIER 2A — Climate Intelligence
ClimateOrchestrator
  Agent 1: TemperatureAgent         current temp vs 90-day avg → anomaly_c
  Agent 2: PrecipitationAgent       rainfall + humidity vs avg → anomaly_mm
  Agent 3: AnomalyDetectorAgent     classifies → LOW/MEDIUM/HIGH/CRITICAL

TIER 2B — Epidemiological Intelligence
EpiOrchestrator
  Agent 4: DiseaseTrackerAgent      historical risk profile by country+disease
  Agent 5: CorrelationAgent         climate anomaly × disease history → score
  Agent 6: PredictionAgent          risk_score, confidence, predicted_window

TIER 2C — Response Intelligence
ResponseOrchestrator
  Agent 7: RiskMapperAgent          high_risk_zones, population_at_risk
  Agent 8: ResourceRecommenderAgent recommended_actions, urgency_level
  Agent 9: AlertPublisherAgent      WHO-style plain-English alert bulletin

## Data Flow
1. main.py calls MainOrchestrator.run(region, lat, lon, country, disease)
2. MainOrchestrator calls ClimateOrchestrator → ClimateReport
3. MainOrchestrator calls EpiOrchestrator(ClimateReport) → EpiReport
4. MainOrchestrator calls ResponseOrchestrator(ClimateReport, EpiReport) → ResponseReport
5. MainOrchestrator merges all three → full_report
6. full_report saved to SQLite
7. full_report printed to terminal and returned

## Agent Input/Output Contracts

Agent 1  TemperatureAgent
  In:  region_name, lat, lon
  Out: region, current_temp_c, historical_avg_temp_c, temp_anomaly_c

Agent 2  PrecipitationAgent
  In:  region_name, lat, lon
  Out: region, current_precip_mm, historical_avg_precip_mm,
       precip_anomaly_mm, current_humidity_pct

Agent 3  AnomalyDetectorAgent
  In:  region_name, temp_anomaly, precip_anomaly, humidity
  Out: anomaly_level, reasoning

Agent 4  DiseaseTrackerAgent
  In:  country, disease
  Out: historical_risk_level, seasonal_peak_months, recent_trend,
       avg_annual_cases_estimate, key_risk_factors

Agent 5  CorrelationAgent
  In:  region_name, disease, country, anomaly_level,
       anomaly_reasoning, disease_profile
  Out: correlation_score, scientific_reasoning

Agent 6  PredictionAgent
  In:  region_name, disease, country, anomaly_level,
       correlation_score, historical_risk_level, recent_trend
  Out: risk_score, confidence, predicted_window, key_factors,
       comparison_to_baseline

Agent 7  RiskMapperAgent
  In:  country, disease, risk_score, lat, lon
  Out: high_risk_zones, population_at_risk_estimate,
       vulnerability_factors, healthcare_capacity

Agent 8  ResourceRecommenderAgent
  In:  country, disease, risk_score, high_risk_zones,
       healthcare_capacity, predicted_window
  Out: recommended_actions, urgency_level, lead_time_weeks,
       estimated_impact

Agent 9  AlertPublisherAgent
  In:  region_name, country, disease, risk_score, confidence,
       predicted_window, anomaly_level, key_factors,
       high_risk_zones, recommended_actions
  Out: alert_text

## Key Design Rules — Never Violate These
1. Every agent returns a Python dict — never a raw string
2. Every agent has a fallback dict — pipeline never crashes on agent failure
3. All Gemini calls go through utils.call_gemini() — never direct
4. All API calls go through utils.safe_api_call() — never direct
5. All JSON parsing goes through utils.parse_json_response() — never manual
6. All constants live in config.py — no hardcoded values in agents
7. All results saved via database.save_prediction() — never direct sqlite3

## Real Data Sources (added v1.1)

A data layer sits below Tier 2 and feeds real live information
into agents before Gemini reasoning happens.

Data layer → Tier 2B:
  data_fetcher.py collects from 4 sources before DiseaseTrackerAgent runs:
    WHO RSS        → real outbreak declarations
    ProMED RSS     → early warning signals (2-4 weeks before WHO)
    ReliefWeb API  → active disaster records
    GDELT API      → global news in real time

Gemini web search grounding:
  CorrelationAgent, PredictionAgent, AlertPublisherAgent all use
  call_gemini_with_search() which gives Gemini live Google access

New output fields added in v1.1:
  active_outbreak      bool  — real surveillance confirmed outbreak
  recent_alert_count   int   — number of real alerts found
  is_real_data         bool  — True means real sources were used
  data_sources         list  — which sources contributed
  real_world_advisories str  — real WHO/CDC advisories found

New files added in v1.1:
  data_fetcher.py      — all 4 real data sources
  utils.call_gemini_with_search() — Gemini live web search

## File Responsibility Map
config.py        all constants and test cases
utils.py         Gemini client, API caller, JSON parser, print helpers
database.py      SQLite init, save, and read functions
main.py          entry point — runs all 5 test cases, prints summary
agents/          9 specialist agents — one class per file
orchestrators/   4 orchestrators — one class per file
tests/           9 unit test files + 1 integration test
docs/            project documentation — never modify during builds
