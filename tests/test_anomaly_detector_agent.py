# tests/test_anomaly_detector_agent.py
# Reference: SKILL_TESTING.md (3 tests per agent, mock everything)

import pytest
from unittest.mock import patch
from agents.anomaly_detector_agent import AnomalyDetectorAgent

@pytest.fixture
def agent():
    return AnomalyDetectorAgent()

def test_anomaly_detector_success(agent):
    """Test SUCCESS: Verifies agent returns correct analysis when Gemini responds perfectly."""
    mock_json = '{"anomaly_level": "HIGH", "reasoning": "Extreme rainfall detected."}'
    
    with patch("agents.anomaly_detector_agent.call_gemini") as mock_call:
        mock_call.return_value = mock_json
        
        result = agent.run("Test Region", 2.5, 150.0, 85.0)
        
        assert result["anomaly_level"] == "HIGH"
        assert "Extreme rainfall" in result["reasoning"]

def test_anomaly_detector_gemini_failure(agent):
    """Test API_FAILURE: Verifies agent handles Gemini failure and returns fallback."""
    with patch("agents.anomaly_detector_agent.call_gemini") as mock_call:
        mock_call.return_value = "" # Simulated failure
        
        result = agent.run("Test Region", 0.0, 0.0, 60.0)
        
        assert result["anomaly_level"] == "MEDIUM" # Fallback
        assert "Unable to assess" in result["reasoning"]

def test_anomaly_detector_malformed_json(agent):
    """Test JSON_MALFORMED: Verifies agent handles garbage JSON string."""
    mock_garbage = "Here is your JSON: {anomaly: 'HIGH', ...} no wait."
    
    with patch("agents.anomaly_detector_agent.call_gemini") as mock_call:
        mock_call.return_value = mock_garbage
        
        result = agent.run("Test Region", 1.0, 10.0, 70.0)
        
        assert result["anomaly_level"] == "MEDIUM" # Fallback from parse_json_response
