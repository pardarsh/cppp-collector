"""
CPPP Tender Collector

Scrapes Central Public Procurement Portal (CPPP) tenders from ePublishing
and eProcurement pages, normalizing them to a canonical procurement schema.

Example:
    from cppp_collector import CPPPCollector

    collector = CPPPCollector()
    tenders = collector.collect_all(epublish_limit=10, eprocure_limit=10)
    for tender in tenders:
        print(f"{tender['identity']['tender_id']}: {tender['procurement']['title']}")
"""

from cppp_collector.collector import CPPPCollector

__version__ = "0.1.0"
__all__ = ["CPPPCollector"]
