# CPPP Collector

Scrape and normalize tender data from India's Central Public Procurement Portal (CPPP).

## Features

- Scrapes **ePublishing** (latest tenders) and **eProcurement** (active tenders) endpoints
- Normalizes data to canonical procurement schema
- Validates output against JSON schema
- Command-line interface for easy data collection
- Python package for programmatic use
- Handles dates, categories, and contract forms intelligently

## Installation

```bash
pip install -e .
```

Or from git:
```bash
pip install git+https://github.com/pardarsh/cppp-collector.git
```

## Quick Start

### Command Line

Collect 5 tenders from each source:
```bash
cppp-collect
```

Collect 20 tenders from ePublishing only:
```bash
cppp-collect --epublish-only --limit 20
```

Save to file:
```bash
cppp-collect --output tenders.json
```

Validate against schema:
```bash
cppp-collect --validate --schema schema.json --output tenders.json
```

### Python API

```python
from cppp_collector import CPPPCollector

# Create collector
collector = CPPPCollector()

# Collect tenders
tenders = collector.collect_all(epublish_limit=10, eprocure_limit=10)

# Use tenders
for tender in tenders:
    print(f"{tender['identity']['tender_id']}: {tender['procurement']['title']}")
    print(f"  Closes: {tender['timeline']['closing_at']}")

# Save to file
collector.save_tenders(tenders, "cppp_tenders.json")
```

## Output Format

Tenders are output in normalized JSON format:

```json
{
  "identity": {
    "tender_id": "BHU/UED/WO/2026-27/90",
    "source": "cppp",
    "source_url": "https://eprocure.gov.in/..."
  },
  "procuring_entity": {
    "organisation": "Government of India (via CPPP)",
    "department": "...",
    "contact": { "email": "...", "phone": "..." }
  },
  "procurement": {
    "title": "SITC of Spare Parts and Comprehensive Servicing...",
    "category": "Supplies",
    "contract_form": "works",
    "estimated_value": { "amount": 850000000, "currency": "INR" }
  },
  "timeline": {
    "closing_at": "2026-10-06T14:00:00Z",
    "opening_at": "2026-10-06T14:30:00Z"
  },
  "metadata": {
    "extracted_at": "2026-10-03T10:07:25Z",
    "extracted_by": "CPPPCollector",
    "extraction_method": "scraper",
    "confidence": 0.85
  }
}
```

## Data Sources

### ePublishing
- **URL**: https://eprocure.gov.in/epublish/app
- **Data**: Latest 10 tenders, basic info (title, dates)
- **Table**: `id="activeTenders"`

### eProcurement
- **URL**: https://www.eprocure.gov.in/eprocure/app
- **Data**: Active tenders with advanced search, richer metadata
- **Status**: May have CAPTCHA protection

## Schema

Tenders conform to `schema_procurement_normalized.json`:

- **Required**: identity, procuring_entity, procurement, timeline, metadata
- **Optional**: documents, eligibility, awards, reference_number, etc.
- **All dates**: ISO 8601 format (UTC) with Z suffix

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black cppp_collector/

# Lint
flake8 cppp_collector/

# Type checking
mypy cppp_collector/
```

## Limitations

- **ePublishing**: Only retrieves 10 latest tenders per run
- **eProcurement**: CAPTCHA-protected; requires session handling
- **Updates**: Re-running collects duplicates; deduplication needed upstream
- **Organization names**: Generic "Government of India" for ePublishing

## Future Improvements

- [ ] Handle eProcurement CAPTCHA with Selenium
- [ ] Implement intelligent deduplication
- [ ] Add support for state procurement portals
- [ ] Add data.gov.in integration
- [ ] Incremental collection (track last collected date)
- [ ] Webhook notifications for new tenders
- [ ] Database backend option

## License

MIT

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Setting up development environment
- Running tests and linting
- Submitting pull requests
- Code of conduct

## Support

For issues, questions, or suggestions, open an issue on GitHub.
