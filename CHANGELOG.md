# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Core CPPP collector with support for ePublishing and eProcurement endpoints
- Tender data normalization to canonical procurement schema
- JSON schema validation for collected tenders
- Command-line interface (`cppp-collect`) for easy data collection
- Python API for programmatic access (`CPPPCollector` class)
- Intelligent date parsing supporting multiple formats (including AM/PM)
- Heuristic category and contract form inference
- Comprehensive test suite (13 unit tests)
- Pre-commit hooks for code quality (black, flake8, isort)
- GitHub Actions CI/CD pipeline for testing and publishing
- Development task management with invoke (cross-platform: Windows, Mac, Linux)
- Professional documentation (README, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT)
- Package publication to PyPI with automated workflow

### Known Limitations
- ePublishing retrieves only 10 latest tenders per run
- eProcurement may be CAPTCHA-protected
- No built-in deduplication (duplicates on re-runs)
- Generic organization names for ePublishing (all "Government of India")

### Future Improvements
- [ ] Handle eProcurement CAPTCHA with Selenium
- [ ] Implement intelligent deduplication
- [ ] Add support for state procurement portals
- [ ] Add data.gov.in integration
- [ ] Incremental collection (track last collected date)
- [ ] Webhook notifications for new tenders
- [ ] Database backend option
