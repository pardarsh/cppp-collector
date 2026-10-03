# Contributing to CPPP Collector

First off, thank you for considering contributing to CPPP Collector! It's people like you that make CPPP Collector such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and the expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguides
* Include appropriate test cases
* End all files with a newline
* Avoid platform-dependent code

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/pardarsh/cppp-collector.git
   cd cppp-collector
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=cppp_collector

# Run specific test file
pytest tests/test_collector.py -v

# Run specific test
pytest tests/test_collector.py::TestDateParsing::test_parse_date_with_am_pm -v
```

## Code Style

We follow PEP 8 style guidelines. The project uses:

* **black** for code formatting
* **flake8** for linting
* **mypy** for type checking

Run these before submitting:

```bash
# Format code
black cppp_collector/ tests/ examples/

# Check style
flake8 cppp_collector/ tests/ examples/

# Type checking
mypy cppp_collector/
```

Or use pre-commit to run all checks:

```bash
pre-commit run --all-files
```

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example:
```
Add support for Maharashtra procurement portal

- Implement MaharashtraCollector class
- Add parser for government website format
- Add 5 unit tests
- Update documentation

Closes #123
```

## Documentation

* Use clear and concise language
* Include examples for new features
* Update README.md if adding user-facing features
* Update docstrings for code changes

## Adding New Collectors

If you're adding support for a new procurement source:

1. Create `cppp_collector/collectors/source_name.py`
2. Implement the collector class following the CPPPCollector pattern
3. Map data to canonical schema
4. Add comprehensive tests in `tests/test_source_name.py`
5. Update README with source information
6. Add example in `examples/`

## Releasing

Maintainers: to release a new version:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a git tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. GitHub Actions will build and publish to PyPI

## Questions?

Feel free to open an issue with the `question` label or contact the maintainers.

## Attribution

This contributing guide is adapted from the [Atom Contributing Guide](https://github.com/atom/atom/blob/master/CONTRIBUTING.md).
