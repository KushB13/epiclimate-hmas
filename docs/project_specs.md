# EpiClimate HMAS — Project Specifications

## Project Identity
- Name: EpiClimate HMAS
- Full title: Climate-Driven Disease Outbreak Prediction Using a
  Hierarchical Multi-Agent AI System
- Student: Kush Bharadiya
- Grade: 8th grade
- Target fair: Dallas Regional Science and Engineering Fair (DRSEF) 2027
- Division: Junior Division (6th–8th grade)
- Category: Computer Science / Systems Software

## Science Fair Rules (DRSEF)
- Follows ISEF rules for Junior Division
- No live internet at the venue (Fair Park, Automobile Building)
- No power outlets — laptop must be battery-powered
- Demo must be a pre-recorded video on a charged laptop
- Physical AND virtual display board required
- Registration deadline: approximately February 12, 2027
- Fair date: approximately February 28, 2027

## Research Question
Can a Hierarchical Multi-Agent AI System that autonomously integrates
real-time climate data with historical epidemiological records predict
the elevated risk of climate-driven disease outbreaks with greater
accuracy and earlier lead time than a historical baseline model?

## Hypothesis
An HMAS correlating climate anomalies with historical outbreak patterns
will correctly identify elevated disease risk at least 4 weeks in advance
with an accuracy greater than 60%, outperforming a baseline model that
uses historical averages alone.

## Variables
- Independent variable: Climate data inputs (temperature anomaly,
  precipitation anomaly, humidity) from 8 weeks prior to each outbreak
- Dependent variable: Prediction accuracy (% of outbreaks correctly
  flagged) and lead time (weeks before outbreak declared)
- Control: Baseline model using only historical average outbreak rates
  with no climate input
- Constants: Same 5 test cases, same 8-week input window, same data
  sources for all tests

## Problem Statement
Climate change is actively expanding disease vectors into new regions.
Over 4 billion people are at risk from climate-sensitive diseases.
Between 2030–2050, climate change is projected to cause 250,000
additional deaths per year. Current early warning systems are reactive —
they alert AFTER outbreaks begin. EpiClimate HMAS predicts outbreaks
BEFORE they happen by reading climate signals weeks in advance.

## Success Criteria
- System runs end-to-end without crashing on all 5 test cases
- Correctly predicts elevated risk in 3 or more of 5 historical cases
- Generates predictions with at least 4-week lead time
- Produces clean, judge-readable terminal output and database records
- Full codebase committed to GitHub with docs and test coverage

## Future Work (post-science-fair roadmap)
- Add vaccination rate data as an additional input variable
- Add population mobility and travel pattern data
- Expand to 20+ diseases and 50+ countries
- Build a public-facing web dashboard
- Publish as a student research paper
