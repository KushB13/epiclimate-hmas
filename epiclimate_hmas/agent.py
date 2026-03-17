import os
import sys

# Ensure the project root is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from google.adk.agents import Agent
from epiclimate_hmas.internal.main_orchestrator.impl import MainOrchestrator

# Standard Python interface for the HMAS
hmas_instance = MainOrchestrator()

# ADK Root Agent definition
root_agent = Agent(
    name="epiclimate_hmas",
    model="gemini-2.0-flash",
    description="EpiClimate Hierarchical Multi-Agent System: Predicts disease outbreaks using climate data and epidemiological surveillance.",
    instruction="""You are the coordinator of the EpiClimate HMAS. 
    
    1. If the user provides a location and a disease, call the 'run' tool immediately.
    2. If the user only provides a location, ask which disease they want to track (default to Dengue if they are unsure).
    3. If the user only provides a disease, ask for the target region/city.
    4. Important: The 'run' tool requires (region_name, lat, lon, country, disease). 
       You MUST find the latitude, longitude, and country for the location using your internal knowledge before calling the tool.
    
    This system will automatically coordinate climate analysis, disease tracking, risk mapping, and response planning.""",
    tools=[hmas_instance.run]
)
