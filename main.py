# main.py
# Reference: docs/experiment_design.md (test case rationale)
# Reference: docs/project_specs.md (science fair context)

import time
from database import init_db
from orchestrators.main_orchestrator import MainOrchestrator
from config import TEST_CASES
from utils import print_section


def main():
    print("\n" + "="*60)
    print("  EPICLIMATE HMAS v1.0")
    print("  Climate-Driven Disease Outbreak Prediction")
    print("  Hierarchical Multi-Agent AI System")
    print("  Gemini 2.0 Flash + Open-Meteo API")
    print("  Science fair project — Kush Bharadiya, DRSEF 2027")
    print("="*60)

    init_db()
    orchestrator = MainOrchestrator()
    results = []

    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n\n{'#'*60}")
        print(f"  TEST CASE {i} of {len(TEST_CASES)}")
        print(f"{'#'*60}")

        result = orchestrator.run(
            region_name=case["region_name"],
            lat=case["lat"], lon=case["lon"],
            country=case["country"], disease=case["disease"]
        )
        results.append(result)

        if i < len(TEST_CASES):
            print(f"\n  [Pausing before next case...]\n")
            time.sleep(3)

    print_section("COMPLETE RUN SUMMARY")
    print(f"  {'Region':<14} {'Disease':<10} {'Risk':<8} {'Conf':<8} {'Urgency'}")
    print(f"  {'-'*52}")
    for r in results:
        print(f"  {r.get('region_name','?'):<14} "
              f"{r.get('disease','?'):<10} "
              f"{str(r.get('risk_score','?'))+'/100':<8} "
              f"{r.get('confidence','?'):<8} "
              f"{r.get('urgency_level','?')}")

    print(f"\n  Results saved to: epiclimate.db")
    print(f"  Predictions logged: {len(results)}")
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
