# SKILL: Test Case Creation — Sustainable Testing Protocol

You are writing tests for EpiClimate HMAS, a 9-agent hierarchical multi-agent system.
The student has limited Gemini API quota. Every test that hits a real API costs real money and quota.
Your job is to write the RIGHT tests — not the most tests.

---

## THE GOLDEN RULE

**3 tests per agent. That's it.**

- 1 happy path (normal working input)
- 1 edge case (weird but valid input)
- 1 failure case (bad input that should be handled gracefully)

Never write more than 3 tests per agent unless a specific bug requires it.
Never write tests that duplicate each other.
Never write a test that calls a real API or real Gemini unless it is the final integration test.

---

## THE TWO TEST TYPES

### Type 1 — Unit Tests (use these 95% of the time)
- Test ONE agent or ONE function in isolation
- ALWAYS mock Gemini and API calls — never hit real endpoints
- Fast, free, no quota used
- Run these constantly during development

### Type 2 — Integration Tests (use these sparingly)
- Test the FULL pipeline end to end with real APIs
- Only run ONCE per session maximum
- Only run when all unit tests already pass
- Use only 1 test region per integration run (not all 5)

---

## FILE STRUCTURE

Create ONE test file per agent. No more.

```
epiclimate-hmas/
└── tests/
    ├── test_temperature_agent.py
    ├── test_precipitation_agent.py
    ├── test_anomaly_detector_agent.py
    ├── test_disease_tracker_agent.py
    ├── test_correlation_agent.py
    ├── test_prediction_agent.py
    ├── test_risk_mapper_agent.py
    ├── test_resource_recommender_agent.py
    ├── test_alert_publisher_agent.py
    ├── test_climate_orchestrator.py
    ├── test_epi_orchestrator.py
    ├── test_response_orchestrator.py
    └── test_integration.py       ← only 1 integration test file, run sparingly
```

---

## THE 3-TEST TEMPLATE

Use this exact pattern for every agent test file. Copy it, change the names.

```python
# tests/test_temperature_agent.py

import pytest
import json
from unittest.mock import patch, MagicMock
from agents.temperature_agent import TemperatureAgent

# ============================================================
# MOCK DATA — define fake API responses here, not inline
# ============================================================

MOCK_OPEN_METEO_RESPONSE = {
    "current": {
        "temperature_2m": 31.2,
        "relative_humidity_2m": 78,
        "precipitation": 5.4,
        "wind_speed_10m": 12.1
    }
}

MOCK_HISTORICAL_RESPONSE = {
    "daily": {
        "temperature_2m_mean": [26.1, 26.8, 27.2, 25.9, 26.5]
    }
}

# ============================================================
# TEST 1 — Happy path: normal valid input
# ============================================================

@patch("agents.temperature_agent.requests.get")
def test_temperature_agent_normal(mock_get):
    """Normal input returns correct anomaly calculation."""
    mock_response = MagicMock()
    mock_response.json.side_effect = [MOCK_OPEN_METEO_RESPONSE, MOCK_HISTORICAL_RESPONSE]
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    agent = TemperatureAgent()
    result = agent.run(region_name="Brazil", lat=-14.2, lon=-51.9)

    assert result["region"] == "Brazil"
    assert "current_temp_c" in result
    assert "historical_avg_temp_c" in result
    assert "temp_anomaly_c" in result
    assert isinstance(result["temp_anomaly_c"], float)
    print(f"[PASS] Normal: anomaly = {result['temp_anomaly_c']}°C")

# ============================================================
# TEST 2 — Edge case: coordinates at equator/zero values
# ============================================================

@patch("agents.temperature_agent.requests.get")
def test_temperature_agent_zero_coords(mock_get):
    """Edge case: coordinates at 0,0 (middle of ocean) — should still return valid JSON."""
    mock_response = MagicMock()
    mock_response.json.side_effect = [MOCK_OPEN_METEO_RESPONSE, MOCK_HISTORICAL_RESPONSE]
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    agent = TemperatureAgent()
    result = agent.run(region_name="TestRegion", lat=0.0, lon=0.0)

    assert result is not None
    assert "temp_anomaly_c" in result
    print("[PASS] Edge case: zero coordinates handled")

# ============================================================
# TEST 3 — Failure case: API returns an error
# ============================================================

@patch("agents.temperature_agent.requests.get")
def test_temperature_agent_api_failure(mock_get):
    """Failure case: API call fails — agent should return defaults, not crash."""
    mock_get.side_effect = Exception("Connection timeout")

    agent = TemperatureAgent()
    result = agent.run(region_name="Brazil", lat=-14.2, lon=-51.9)

    # Should return something, not raise an exception
    assert result is not None
    assert "region" in result
    print("[PASS] Failure case: API error handled gracefully")
```

---

## MOCK PATTERNS — copy these exactly

### Mocking requests.get (for Open-Meteo):
```python
from unittest.mock import patch, MagicMock

@patch("agents.temperature_agent.requests.get")
def test_something(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"your": "fake_data"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    # your test here
```

### Mocking Gemini (for agents that use LLM):
```python
from unittest.mock import patch

MOCK_GEMINI_JSON = '{"anomaly_level": "HIGH", "reasoning": "Mock reasoning for testing"}'

@patch("agents.anomaly_detector_agent.call_gemini")
def test_anomaly_detector(mock_gemini):
    mock_gemini.return_value = MOCK_GEMINI_JSON
    # your test here
```

### Mocking multiple API calls in sequence:
```python
mock_response.json.side_effect = [
    FIRST_API_RESPONSE,    # returned on first call to .json()
    SECOND_API_RESPONSE    # returned on second call to .json()
]
```

---

## INTEGRATION TEST — run sparingly, once per session max

```python
# tests/test_integration.py
# WARNING: This test hits real APIs and uses real Gemini quota.
# Only run when ALL unit tests pass.
# Only run ONCE per session.

import pytest
from orchestrators.main_orchestrator import MainOrchestrator

@pytest.mark.integration
def test_full_pipeline_brazil_dengue():
    """
    Full end-to-end pipeline test.
    Uses real Open-Meteo API + real Gemini.
    Run once to validate the full system works.
    """
    orchestrator = MainOrchestrator()
    result = orchestrator.run(
        region_name="Brazil",
        lat=-14.2,
        lon=-51.9,
        country="Brazil",
        disease="dengue"
    )

    # Only check structure — not exact values (Gemini responses vary)
    assert result is not None
    assert "risk_score" in result
    assert "alert_text" in result
    assert isinstance(result["risk_score"], int)
    assert 0 <= result["risk_score"] <= 100
    assert len(result["alert_text"]) > 10

    print(f"\n[INTEGRATION PASS]")
    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Confidence: {result.get('confidence', 'N/A')}")
    print(f"Alert: {result['alert_text'][:100]}...")
```

Run integration tests with:
```bash
pytest tests/test_integration.py -v -m integration
```

Run unit tests only (no API calls):
```bash
pytest tests/ -v --ignore=tests/test_integration.py
```

---

## QUOTA BUDGET PER SESSION

| Test Type | Gemini Calls | API Calls | When to Run |
|---|---|---|---|
| Unit tests (all 9 agents) | 0 | 0 | Every time you code |
| Orchestrator unit tests | 0 | 0 | Every time you code |
| Integration test (1 region) | ~9 | ~2 | Once per session max |
| Full 5-region experiment | ~45 | ~10 | Only for science fair data |

**Never run the full 5-region experiment during development.**
Save that for when the entire system is complete and tested.

---

## WHAT MAKES A GOOD TEST ASSERTION

Good assertions check structure AND values:
```python
# GOOD — checks it exists AND is the right type AND is in valid range
assert "risk_score" in result
assert isinstance(result["risk_score"], int)
assert 0 <= result["risk_score"] <= 100

# BAD — too brittle, will break when Gemini changes its wording
assert result["reasoning"] == "High temperature anomaly detected"
```

For Gemini outputs, never assert exact text. Only assert:
- The key exists in the dict
- The value is the right type (str, int, list, etc.)
- Numbers are in a valid range
- Lists are not empty

---

## HOW TO RUN TESTS

Install pytest once:
```bash
pip install pytest
```

Run all unit tests:
```bash
pytest tests/ -v --ignore=tests/test_integration.py
```

Run one specific agent test:
```bash
pytest tests/test_temperature_agent.py -v
```

Run with print output visible:
```bash
pytest tests/ -v -s --ignore=tests/test_integration.py
```

---

## WHEN TO WRITE A NEW TEST

Only add a new test when:
1. You fixed a bug — write a test that would have caught it
2. You added a new feature or new agent
3. A judge or mentor asks "how did you verify this works?"

Do NOT add new tests because:
- You want more coverage
- You're not sure if something works (just run the existing tests)
- You're bored

---

## TEST NAMING CONVENTION

Always name tests like this:
```
test_[agent_name]_[scenario]
```

Examples:
- `test_temperature_agent_normal`
- `test_temperature_agent_api_failure`
- `test_prediction_agent_high_correlation`
- `test_alert_publisher_empty_input`

---

*This skill file governs all test creation for EpiClimate HMAS. Read it before writing any test.*