"""Development tasks using Invoke.

Works on Windows, Mac, Linux without any special setup.
Install: pip install invoke

Usage:
    invoke --list              # List all tasks
    invoke install             # Install package
    invoke dev                 # Install with dev dependencies
    invoke test                # Run tests
    invoke test-cov            # Tests with coverage
    invoke lint                # Run flake8
    invoke format              # Format code with black + isort
    invoke check               # Run all checks
    invoke pre-commit          # Install/run pre-commit
    invoke clean               # Clean build artifacts
    invoke collect             # Collect tenders from CPPP
    invoke build               # Build distribution
    invoke publish             # Publish to PyPI
"""

import shutil
from pathlib import Path

from invoke import Context, task  # type: ignore


@task
def install(c: Context) -> None:
    """Install package."""
    c.run("pip install -e .")
    print("success: Package installed")


@task
def dev(c: Context) -> None:
    """Install in development mode with dev dependencies."""
    c.run('pip install -e ".[dev]"')
    print("success: Dev dependencies installed")


@task
def test(c: Context) -> None:
    """Run tests."""
    c.run("pytest tests/ -v")


@task
def test_cov(c: Context) -> None:
    """Run tests with coverage report."""
    c.run(
        "pytest tests/ -v --cov=cppp_collector "
        "--cov-report=term-missing --cov-report=html"
    )
    print("success: Coverage report generated in htmlcov/index.html")


@task
def lint(c: Context) -> None:
    """Run flake8 linter."""
    c.run("flake8 cppp_collector tests examples")


@task
def format(c: Context) -> None:
    """Format code with black and isort."""
    c.run("black cppp_collector tests examples")
    c.run("isort cppp_collector tests examples")
    print("success: Code formatted")


@task
def type_check(c: Context) -> None:
    """Run mypy type checker."""
    c.run("mypy cppp_collector --ignore-missing-imports")


@task(pre=[lint])  # type: ignore
def check(c: Context) -> None:
    """Run all checks (lint and formatting)."""
    print("success: All checks passed!")


@task
def pre_commit(c: Context) -> None:
    """Install and run pre-commit hooks."""
    c.run("pre-commit install")
    c.run("pre-commit run --all-files")
    print("success: Pre-commit hooks installed")


@task
def clean(c: Context) -> None:
    """Remove build artifacts and cache."""
    dirs_to_remove = [
        "build",
        "dist",
        ".eggs",
        ".pytest_cache",
        ".mypy_cache",
        ".coverage",
        "htmlcov",
    ]

    for dir_name in dirs_to_remove:
        dir_path = Path(dir_name)
        if dir_path.exists():
            if dir_path.is_dir():
                shutil.rmtree(dir_path)
            else:
                dir_path.unlink()
            print(f"Removed {dir_name}")

    # Remove __pycache__ directories
    for pycache in Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache)
        print(f"Removed {pycache}")

    # Remove .pyc files
    for pyc in Path(".").rglob("*.pyc"):
        pyc.unlink()

    # Remove *.egg-info
    for egg in Path(".").glob("*.egg-info"):
        shutil.rmtree(egg)
        print(f"Removed {egg}")

    print("success: Clean complete")


@task
def collect(c: Context) -> None:
    """Collect tenders from CPPP."""
    c.run("cppp-collect --limit 10")


@task
def collect_save(c: Context) -> None:
    """Collect and save tenders to file."""
    c.run("cppp-collect --limit 10 --output tenders.json")


@task(pre=[clean])  # type: ignore
def build(c: Context) -> None:
    """Build distribution packages."""
    c.run("pip install build")
    c.run("python -m build")
    print("success: Distribution built in dist/")


@task(pre=[build])  # type: ignore
def publish(c: Context) -> None:
    """Publish to PyPI (requires PYPI_API_TOKEN)."""
    c.run("pip install twine")
    c.run("twine upload dist/*")
    print("success: Published to PyPI")


@task(pre=[build])  # type: ignore
def publish_test(c: Context) -> None:
    """Publish to TestPyPI (requires PYPI_API_TOKEN)."""
    c.run("pip install twine")
    c.run("twine upload --repository testpypi dist/*")
    print("success: Published to TestPyPI")
