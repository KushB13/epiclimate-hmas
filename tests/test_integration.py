# tests/test_integration.py
# Reference: SKILL_TESTING.md (Rule 3: Only test_integration.py uses real APIs)

import pytest
from epiclimate_hmas.agent import MainOrchestrator
from database import init_db

@pytest.mark.integration
def test_full_pipeline_brazil_dengue():
    """
    Integration test: Runs the full pipeline for Brazil/Dengue.
    Requires GEMINI_API_KEY in .env.
    """
    init_db()
    orch = MainOrchestrator()
    
    # Using a subset of the actual test case
    result = orch.run(
        region_name="IntegrationTest_Brazil",
        lat=-14.2, lon=-51.9,
        country="Brazil", disease="dengue"
    )
    
    assert result["region_name"] == "IntegrationTest_Brazil"
    assert "risk_score" in result
    assert "alert_text" in result
    assert result["risk_score"] >= 0 and result["risk_score"] <= 100
