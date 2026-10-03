#!/usr/bin/env python3
"""
Example: Validate collected tenders against schema
"""

import json
from pathlib import Path

from cppp_collector.collector import CPPPCollector
from cppp_collector.validator import validate_tenders

# Collect tenders
print("Collecting tenders...")
collector = CPPPCollector()
tenders = collector.collect_all(epublish_limit=10, eprocure_limit=0)

# Load schema (you would provide your own schema file)
schema_file = Path("schema.json")

if not schema_file.exists():
    print(f"Schema file not found: {schema_file}")
    print("Skipping validation.")
else:
    with open(schema_file) as f:
        schema = json.load(f)

    print(f"\nValidating {len(tenders)} tenders...")

    errors = validate_tenders(tenders, schema)

    if errors:
        print(f"\n[FAIL] {len(errors)} validation errors:\n")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"\n[OK] All {len(tenders)} tenders are valid!")

    # Save validated tenders
    collector.save_tenders(tenders, "validated_tenders.json")
