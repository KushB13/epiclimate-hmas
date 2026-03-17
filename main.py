# main.py
# Reference: docs/experiment_design.md (test case rationale)
# Reference: docs/project_specs.md (science fair context)

import sys
from database import init_db
from epiclimate_hmas.agent import MainOrchestrator
from utils import print_section, geocode_location


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

    while True:
        print_section("HMAS INTERACTIVE MODE")
        print("  Enter details for a new prediction (or type 'quit' to exit).")
        
        region_name = input("\n  Target Location (e.g., Lima, Peru): ").strip()
        if region_name.lower() in ["quit", "exit", "q"]:
            break
            
        disease = input("  Target Disease (e.g., Dengue): ").strip()
        if not disease:
            disease = "Dengue" # Default
            print(f"  [Using default: {disease}]")

        print(f"  [Geocoding '{region_name}'...]")
        lat, lon, country = geocode_location(region_name)

        if lat is None:
            print(f"  [ERROR] Could not find coordinates for '{region_name}'.")
            print("  Please try a more specific name (e.g., 'City, Country').")
            continue

        print(f"  [Found: {country} | Lat: {lat}, Lon: {lon}]")
        
        try:
            orchestrator.run(
                region_name=region_name,
                lat=lat, lon=lon,
                country=country if country else region_name, 
                disease=disease
            )
        except KeyboardInterrupt:
            print("\n  [Prediction Interrupted]")
        except Exception as e:
            print(f"\n  [ERROR] Prediction failed: {e}")

        print("\n" + "-"*60)
        choice = input("  Run another? (y/n): ").lower()
        if choice.startswith('n'):
            break

    print("\n  Thank you for using EpiClimate HMAS. Results are saved in epiclimate.db.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
