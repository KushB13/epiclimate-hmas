# app/epiclimate_hmas/agent.py
import sys
import os
from google.adk.agents import Agent

# Add project root to path so we can import orchestrators
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from orchestrators.climate_orchestrator import ClimateOrchestrator
from orchestrators.epi_orchestrator import EpiOrchestrator
from orchestrators.response_orchestrator import ResponseOrchestrator
from orchestrators.main_orchestrator import MainOrchestrator

# Initialize orchestrators
climate_orch = ClimateOrchestrator()
epi_orch     = EpiOrchestrator()
resp_orch    = ResponseOrchestrator()
main_orch    = MainOrchestrator()

def get_climate_data(region_name: str, lat: float, lon: float) -> dict:
    """Fetches and analyzes climate anomalies for a given location."""
    return climate_orch.run(region_name, lat, lon)

def get_epi_analysis(climate_report: dict, country: str, disease: str) -> dict:
    """Analyzes epidemiological risk based on climate data and disease profiles."""
    return epi_orch.run(climate_report, country, disease)

def get_response_plan(climate_report: dict, epi_report: dict) -> dict:
    """Generates public health response recommendations and risk maps."""
    return resp_orch.run(climate_report, epi_report)

def run_full_prediction(region_name: str, lat: float, lon: float, country: str, disease: str) -> dict:
    """Runs the entire Hierarchical Multi-Agent System (HMAS) pipeline to predict an outbreak."""
    return main_orch.run(region_name, lat, lon, country, disease)

# Define the Root Agent for ADK
root_agent = Agent(
    name="epiclimate_hmas_master",
    model="gemini-1.5-flash",
    description="Master Orchestrator for the EpiClimate Hierarchical Multi-Agent System.",
    instruction=(
        "You are the master intelligence for EpiClimate HMAS. Your goal is to predict "
        "disease outbreaks using climate data and epidemiological intelligence. "
        "You have access to specialized tools for Climate, Epidemiology, and Response tiers. "
        "You can either run the full pipeline or individual tiers as requested by the user. "
        "When providing reports, be concise, data-driven, and highlight the risk score and urgency."
    ),
    tools=[
        get_climate_data,
        get_epi_analysis,
        get_response_plan,
        run_full_prediction
    ]
)
