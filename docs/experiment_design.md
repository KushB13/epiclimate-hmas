# EpiClimate HMAS — Experiment Design

## Overview
This experiment tests whether EpiClimate HMAS can predict historical
disease outbreaks using only climate data from the 8-week window
BEFORE each outbreak was officially declared — before any human
knew the outbreak was coming.

## Method
For each of the 5 test cases:
1. Collect the climate data (temperature, precipitation, humidity) from
   the 8-week window BEFORE the outbreak was officially declared
2. Run that climate data through EpiClimate HMAS
3. Record the system's predicted risk score (0-100) and confidence
4. Compare against a baseline: simple historical average outbreak risk
   with no climate input

## 5 Test Cases

Case 1  Brazil      Dengue    2024  Feb 2024 — record 7.6M cases
Case 2  Sudan       Cholera   2023  Jun 2023 — 252,000+ cases
Case 3  Kenya       Malaria   2023  Aug 2023 — spike in highlands
Case 4  Bangladesh  Dengue    2023  Jul 2023 — worst in decades
Case 5  Mozambique  Cholera   2023  Mar 2023 — post-cyclone outbreak

## Scoring a Prediction

Risk score >= 60 AND outbreak occurred     = TRUE POSITIVE  (correct)
Risk score <  60 AND outbreak occurred     = FALSE NEGATIVE (missed)
Risk score >= 60 AND no outbreak occurred  = FALSE POSITIVE (false alarm)
Risk score <  60 AND no outbreak occurred  = TRUE NEGATIVE  (correct)

## Baseline Model
The baseline does NOT use climate data.
Assigns risk based only on:
  - Historical average outbreak frequency for that disease in that country
  - Month of year (seasonal baseline)
This represents a simple lookup table with no AI.

## Metrics to Report
1. HMAS accuracy:        (true positives / 5) x 100%
2. Baseline accuracy:    (baseline correct / 5) x 100%
3. Improvement:          HMAS accuracy minus baseline accuracy
4. Average risk score:   mean of risk_score across all 5 cases
5. Average lead time:    mean weeks before outbreak that score >= 60

## Data Storage
All results auto-saved to epiclimate.db.
Export with:
  python -c "from database import get_all_predictions; import json; print(json.dumps(get_all_predictions(), indent=2))"

## Target Result
HMAS predicts 3+ of 5 outbreaks correctly (60%+ accuracy)
with average lead time of 4+ weeks.
Baseline expected to predict 2 of 5 (40% accuracy).
