#!/usr/bin/env python3
"""
Basic usage example for CPPP Collector
"""

from cppp_collector import CPPPCollector

# Create collector
collector = CPPPCollector()

# Collect tenders
print("Collecting tenders from CPPP...")
tenders = collector.collect_all(epublish_limit=5, eprocure_limit=5)

# Print results
print(f"\nCollected {len(tenders)} tenders:\n")

for i, tender in enumerate(tenders, 1):
    tender_id = tender["identity"]["tender_id"]
    title = tender["procurement"]["title"]
    closing = tender["timeline"]["closing_at"] or "N/A"

    print(f"{i}. {tender_id}")
    print(f"   Title: {title[:60]}...")
    print(f"   Closes: {closing}\n")

# Save to file
if tenders:
    filepath = collector.save_tenders(tenders, "example_tenders.json")
    print(f"\nSaved to: {filepath}")
