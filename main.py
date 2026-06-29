# main.py
# Run this file to test everything today

import json
import os
from sw_connection import SolidWorksConnection
from extractor import DimensionExtractor


PART_PATH = r"C:\Users\Mansi\OneDrive\Desktop\Internship\Solidworks-agent\sheet-metal-part3.SLDPRT"

# Dynamically name the output JSON file based on the part filename
part_filename = os.path.splitext(os.path.basename(PART_PATH))[0]
OUTPUT_PATH = os.path.join(r"C:\Users\Mansi\OneDrive\Desktop\part2\output", f"dimensions_{part_filename}.json")

def main():
    print("=" * 50)
    print("SolidWorks Dimension Extractor")
    print("=" * 50)

    # Step 1 — Connect to SolidWorks
    print("\nStep 1: Connecting to SolidWorks...")
    sw = SolidWorksConnection() ##creating SolidworksConnection obj
    sw.connect() ##connect to solidworks using COM

    # Step 2 — Open the part
    print(f"\nStep 2: Opening part...")
    part_doc = sw.open_part(PART_PATH) ##com object

    # Step 3 — Extract entire model tree
    print(f"\nStep 3: Extracting model tree...")
    extractor = DimensionExtractor(part_doc)
    data      = extractor.extract()

    # Step 4 — Print results to console
    print("\n" + "=" * 50)
    print(f"RESULTS — {data['part_name']}")
    print("=" * 50)
    print(f"Total features: {data['total_features']}")
    print(f"Total dimensions: {data['total_dims']}")
    print()

    for feat in data["features"]:
        print(f"  [{feat['feature_type']}] {feat['feature_name']}")
        if feat["dimensions"]:
            for d in feat["dimensions"]:
                unit_str = f" {d['unit']}" if d['unit'] else ""
                print(f"       -> {d['type']:12} {d['name']:25} = {d['value']}{unit_str}")
        else:
            print(f"       -> no dimensions found")
        print()

    # Step 5 — Save to JSON file
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()