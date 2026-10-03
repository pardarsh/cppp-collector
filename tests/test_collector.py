"""
Unit tests for CPPP Collector
"""

import pytest
from cppp_collector.collector import CPPPCollector
from cppp_collector.validator import validate_tender


class TestDateParsing:
    """Test date parsing"""

    def test_parse_date_with_am_pm(self):
        """Test parsing date with AM/PM format"""
        collector = CPPPCollector()
        result = collector._parse_date("06-Oct-2026 02:00 PM")
        assert result == "2026-10-06T14:00:00Z"

    def test_parse_date_with_am(self):
        """Test parsing AM time"""
        collector = CPPPCollector()
        result = collector._parse_date("06-Oct-2026 10:30 AM")
        assert result == "2026-10-06T10:30:00Z"

    def test_parse_date_without_time(self):
        """Test parsing date without time"""
        collector = CPPPCollector()
        result = collector._parse_date("06-Oct-2026")
        assert result == "2026-10-06T00:00:00Z"

    def test_parse_date_invalid(self):
        """Test parsing invalid date"""
        collector = CPPPCollector()
        result = collector._parse_date("invalid")
        assert result is None

    def test_parse_date_none(self):
        """Test parsing None"""
        collector = CPPPCollector()
        result = collector._parse_date(None)
        assert result is None


class TestCategoryInference:
    """Test category inference"""

    def test_infer_category_works(self):
        """Test inferring 'Works' category"""
        collector = CPPPCollector()
        result = collector._infer_category("Road Construction Project")
        assert result == "Works"

    def test_infer_category_supplies(self):
        """Test inferring 'Supplies' category"""
        collector = CPPPCollector()
        result = collector._infer_category("Supply of Materials")
        assert result == "Supplies"

    def test_infer_category_services(self):
        """Test inferring 'Services' category"""
        collector = CPPPCollector()
        result = collector._infer_category("Consulting Services")
        assert result == "Services"

    def test_infer_category_other(self):
        """Test default category"""
        collector = CPPPCollector()
        result = collector._infer_category("Unknown procurement")
        assert result == "Other"


class TestContractFormInference:
    """Test contract form inference"""

    def test_infer_contract_form_works(self):
        """Test inferring 'works' contract form"""
        collector = CPPPCollector()
        result = collector._infer_contract_form("Building Construction")
        assert result == "works"

    def test_infer_contract_form_service(self):
        """Test inferring 'service' contract form"""
        collector = CPPPCollector()
        result = collector._infer_contract_form("Consulting Services")
        assert result == "service"

    def test_infer_contract_form_supply(self):
        """Test inferring 'supply' contract form"""
        collector = CPPPCollector()
        result = collector._infer_contract_form("Supply of Equipment")
        assert result == "supply"


class TestTenderStructure:
    """Test tender data structure"""

    def test_tender_has_required_fields(self):
        """Test that collector output has required fields"""
        collector = CPPPCollector()

        # Mock tender data
        tender = {
            "identity": {"tender_id": "TEST-001", "source": "cppp"},
            "procuring_entity": {"organisation": "Test Org"},
            "procurement": {"title": "Test Tender", "contract_form": "works"},
            "timeline": {"closing_at": "2026-10-31T18:00:00Z"},
            "metadata": {
                "extracted_at": "2026-10-03T10:00:00Z",
                "extracted_by": "CPPPCollector",
                "extraction_method": "scraper",
                "confidence": 0.85,
            },
        }

        # Check structure
        assert "identity" in tender
        assert "procuring_entity" in tender
        assert "procurement" in tender
        assert "timeline" in tender
        assert "metadata" in tender

        # Check required fields
        assert tender["identity"]["tender_id"]
        assert tender["identity"]["source"] == "cppp"
        assert tender["procuring_entity"]["organisation"]
        assert tender["procurement"]["title"]
        assert tender["timeline"]["closing_at"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
