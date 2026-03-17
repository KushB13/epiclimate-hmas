# tests/test_temperature_agent.py
# Reference: SKILL_TESTING.md (3 tests per agent, mock everything)

import pytest
from unittest.mock import patch
from epiclimate_hmas.internal.temperature_agent.impl import TemperatureAgent

@pytest.fixture
def agent():
    return TemperatureAgent()

def test_temperature_agent_success(agent):
    """Test SUCCESS: Verifies agent returns correct data when APIs respond perfectly."""
    mock_current = {"current": {"temperature_2m": 30.5}}
    mock_archive = {"daily": {"temperature_2m_mean": [25.0, 26.0, 24.0]}}
    
    with patch("epiclimate_hmas.internal.temperature_agent.impl.safe_api_call") as mock_safe_call:
        mock_safe_call.side_effect = [mock_current, mock_archive]
        
        result = agent.run("Test Region", 0.0, 0.0)
        
        assert result["current_temp_c"] == 30.5
        assert result["historical_avg_temp_c"] == 25.0
        assert result["temp_anomaly_c"] == 5.5
        assert "temp_error" not in result

def test_temperature_agent_api_failure(agent):
    """Test API_FAILURE: Verifies agent handles failure and returns fallback."""
    with patch("epiclimate_hmas.internal.temperature_agent.impl.safe_api_call") as mock_safe_call:
        mock_safe_call.return_value = {} # Simulated failure
        
        result = agent.run("Test Region", 0.0, 0.0)
        
        assert result["current_temp_c"] == 25.0 # Fallback
        assert result["historical_avg_temp_c"] == 25.0
        assert result["temp_anomaly_c"] == 0.0
        assert "temp_error" in result

def test_temperature_agent_archive_missing(agent):
    """Test ARCHIVE_MISSING: Verifies agent handles missing archive data."""
    mock_current = {"current": {"temperature_2m": 28.0}}
    
    with patch("epiclimate_hmas.internal.temperature_agent.impl.safe_api_call") as mock_safe_call:
        mock_safe_call.side_effect = [mock_current, {}]
        
        result = agent.run("Test Region", 0.0, 0.0)
        
        assert result["current_temp_c"] == 28.0
        assert result["historical_avg_temp_c"] == 25.0 # Default
        assert result["temp_anomaly_c"] == 3.0
