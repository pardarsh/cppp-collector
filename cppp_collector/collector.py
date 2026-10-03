"""
CPPP Tender Collector

Scrapes Central Public Procurement Portal (CPPP) tenders from:
- ePublishing: Latest tenders
- eProcurement: Active tenders with advanced search

Outputs normalized procurement data (schema_procurement_normalized.json format)
"""

import json
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class CPPPCollector:
    """Collects tender data from CPPP ePublishing and eProcurement"""

    BASE_URL_EPUBLISH = "https://eprocure.gov.in/epublish/app"
    BASE_URL_EPROCURE = "https://www.eprocure.gov.in/eprocure/app"

    def __init__(self, output_dir: str = "data/raw/cppp"):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "CPPP-Collector/1.0 (+https://github.com/yourusername/cppp-collector)"
            }
        )
        self.output_dir = output_dir

    def collect_from_epublishing(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Collect tenders from CPPP ePublishing (latest tenders)

        Args:
            limit: Maximum number of tenders to collect

        Returns:
            List of normalized procurement records
        """
        print(f"[CPPP ePublishing] Fetching latest {limit} tenders...")
        tenders = []

        try:
            # Fetch ePublishing page (no params - params cause redirect to minimal page)
            response = self.session.get(self.BASE_URL_EPUBLISH, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find the active tenders table (id="activeTenders")
            tender_table = soup.find("table", id="activeTenders")
            if not tender_table:
                print("  [!] Could not find tenders table")
                return tenders

            # Get all rows from the table
            tender_rows = tender_table.find_all("tr")

            for i, row in enumerate(tender_rows[:limit]):
                try:
                    tender = self._parse_epublishing_row(row)
                    if tender:
                        tenders.append(tender)
                except Exception as e:
                    print(f"  [WARN] Error parsing row {i}: {e}")
                    continue

            print(f"  [OK] Collected {len(tenders)} tenders from ePublishing")

        except requests.RequestException as e:
            print(f"  [FAIL] Failed to fetch ePublishing: {e}")

        return tenders

    def collect_from_eprocurement(
        self, search_params: Optional[Dict] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Collect tenders from CPPP eProcurement (active tenders)

        Note: eProcurement has CAPTCHA protection. This collector attempts to:
        1. Parse publicly cached versions
        2. Use session cookies if available
        3. Fall back to advanced search if interactive search unavailable

        Args:
            search_params: Optional search filters (category, state, etc.)
            limit: Maximum number of tenders to collect

        Returns:
            List of normalized procurement records
        """
        print(f"[CPPP eProcurement] Fetching active tenders (limit: {limit})...")
        tenders = []

        try:
            # Advanced search page with proper query params
            response = self.session.get(
                self.BASE_URL_EPROCURE,
                params={"page": "FrontEndAdvancedSearch"},
                timeout=10,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Advanced search provides more metadata
            tender_rows = soup.find_all("tr", class_=re.compile("result|tender", re.I))

            for i, row in enumerate(tender_rows[:limit]):
                try:
                    tender = self._parse_eprocurement_row(row)
                    if tender:
                        tenders.append(tender)
                except Exception as e:
                    print(f"  [WARN] Error parsing row {i}: {e}")
                    continue

            print(f"  [OK] Collected {len(tenders)} tenders from eProcurement")

        except requests.RequestException as e:
            print(f"  [FAIL] Failed to fetch eProcurement: {e}")
            print(
                "  Note: eProcurement may have CAPTCHA protection or session requirements"
            )

        return tenders

    def _parse_epublishing_row(self, row: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """Parse a tender row from ePublishing"""
        cells = row.find_all("td")
        if len(cells) < 4:
            return None

        # Extract fields from cells: Title, RefNo, ClosingDate, OpeningDate
        title_cell = cells[0].get_text(strip=True)
        ref_no = cells[1].get_text(strip=True)
        closing_date = cells[2].get_text(strip=True)
        opening_date = cells[3].get_text(strip=True)

        # Remove numbering prefix from title (e.g., "1. Title" -> "Title")
        title = re.sub(r"^\d+\.\s+", "", title_cell)

        if not ref_no or not title:
            return None

        # Find tender link for URL
        tender_link = row.find("a", href=True)
        source_url = (
            urljoin(self.BASE_URL_EPUBLISH, tender_link["href"])
            if tender_link
            else None
        )

        return {
            "identity": {
                "tender_id": ref_no,
                "source": "cppp",
                "source_url": source_url,
            },
            "procuring_entity": {
                "organisation": "Government of India (via CPPP)",
            },
            "procurement": {
                "title": title,
                "contract_form": self._infer_contract_form(title),
            },
            "timeline": {
                "closing_at": self._parse_date(closing_date),
                "opening_at": self._parse_date(opening_date),
            },
            "metadata": {
                "extracted_at": datetime.utcnow().isoformat() + "Z",
                "extracted_by": "CPPPCollector",
                "extraction_method": "scraper",
                "confidence": 0.85,
            },
        }

    def _parse_eprocurement_row(self, row: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """Parse a tender row from eProcurement advanced search"""
        cells = row.find_all("td")
        if len(cells) < 3:
            return None

        # Advanced search provides richer metadata
        tender_id = cells[0].get_text(strip=True) if len(cells) > 0 else None
        title = cells[1].get_text(strip=True) if len(cells) > 1 else None
        organisation = cells[2].get_text(strip=True) if len(cells) > 2 else None
        category = cells[3].get_text(strip=True) if len(cells) > 3 else None
        closing_date = cells[4].get_text(strip=True) if len(cells) > 4 else None

        if not tender_id or not title:
            return None

        return {
            "identity": {
                "tender_id": tender_id,
                "source": "cppp",
                "source_url": None,  # Would need to construct from tender details page
            },
            "procuring_entity": {"organisation": organisation},
            "procurement": {
                "title": title,
                "category": category or self._infer_category(title),
                "contract_form": self._infer_contract_form(title),
            },
            "timeline": {"closing_at": self._parse_date(closing_date)},
            "metadata": {
                "extracted_at": datetime.utcnow().isoformat() + "Z",
                "extracted_by": "CPPPCollector",
                "extraction_method": "scraper",
                "confidence": 0.8,
            },
        }

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[str]:
        """Parse date string to ISO format"""
        if not date_str:
            return None

        date_str = date_str.strip()

        # Try common Indian date formats including AM/PM
        formats = [
            "%d-%b-%Y %I:%M %p",  # 06-Oct-2026 02:00 PM
            "%d-%m-%Y %H:%M",     # 06-10-2026 14:00
            "%d/%m/%Y %H:%M",     # 06/10/2026 14:00
            "%d-%b-%Y",           # 06-Oct-2026
            "%d-%m-%Y",           # 06-10-2026
            "%d/%m/%Y",           # 06/10/2026
            "%Y-%m-%d",           # 2026-10-06
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.isoformat() + "Z"
            except ValueError:
                continue

        return None

    @staticmethod
    def _infer_category(title: str) -> str:
        """Infer procurement category from title"""
        title_lower = title.lower()

        if any(
            word in title_lower
            for word in ["construction", "road", "bridge", "highway"]
        ):
            return "Works"
        elif any(word in title_lower for word in ["supply", "purchase", "material"]):
            return "Supplies"
        elif any(
            word in title_lower for word in ["service", "consultant", "maintenance"]
        ):
            return "Services"

        return "Other"

    @staticmethod
    def _infer_contract_form(title: str) -> str:
        """Infer contract form from title"""
        title_lower = title.lower()

        if any(word in title_lower for word in ["construction", "works", "building"]):
            return "works"
        elif any(word in title_lower for word in ["service", "consulting"]):
            return "service"
        elif any(word in title_lower for word in ["supply", "purchase"]):
            return "supply"

        return "works"

    def save_tenders(
        self, tenders: List[Dict[str, Any]], filename: str = "cppp_tenders.json"
    ):
        """Save collected tenders to JSON file"""
        import os

        os.makedirs(self.output_dir, exist_ok=True)

        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(tenders, f, indent=2, ensure_ascii=False)

        print(f"[OK] Saved {len(tenders)} tenders to {filepath}")

        return filepath

    def collect_all(
        self, epublish_limit: int = 5, eprocure_limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Collect from both ePublishing and eProcurement"""
        print("\n=== CPPP Tender Collection ===\n")

        all_tenders = []

        # Collect from ePublishing
        epublish_tenders = self.collect_from_epublishing(limit=epublish_limit)
        all_tenders.extend(epublish_tenders)

        time.sleep(1)  # Be respectful to the server

        # Collect from eProcurement
        eprocure_tenders = self.collect_from_eprocurement(limit=eprocure_limit)
        all_tenders.extend(eprocure_tenders)

        print(f"\n[OK] Total collected: {len(all_tenders)} tenders")

        return all_tenders
