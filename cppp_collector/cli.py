"""
Command-line interface for CPPP Collector

Usage:
    cppp-collect                             # Collect 5 from each source
    cppp-collect --limit 10                  # Collect 10 from each source
    cppp-collect --epublish-only             # Only ePublishing
    cppp-collect --output tenders.json       # Save to file
    cppp-collect --validate                  # Validate against schema
"""

import argparse
import json
import sys
from pathlib import Path

from cppp_collector.collector import CPPPCollector
from cppp_collector.validator import validate_tenders


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="cppp-collect",
        description="Collect and output normalized CPPP tender data",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of tenders to collect from each source (default: 5)",
    )
    parser.add_argument(
        "--epublish-only",
        action="store_true",
        help="Only collect from ePublishing (not eProcurement)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Save to file instead of stdout",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate output against schema",
    )
    parser.add_argument(
        "--schema",
        type=str,
        default=None,
        help="Path to schema JSON file (required with --validate)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Pretty-print JSON (default: True)",
    )

    args = parser.parse_args()

    # Collect tenders
    collector = CPPPCollector()

    if args.epublish_only:
        print(f"Collecting {args.limit} tenders from ePublishing...", flush=True)
        tenders = collector.collect_from_epublishing(limit=args.limit)
    else:
        print(
            f"Collecting {args.limit} tenders from each source...",
            flush=True,
        )
        tenders = collector.collect_all(
            epublish_limit=args.limit, eprocure_limit=args.limit
        )

    # Validate if requested
    if args.validate:
        if not args.schema:
            print(
                "error: --schema required with --validate",
                file=sys.stderr,
            )
            sys.exit(1)

        schema_path = Path(args.schema)
        if not schema_path.exists():
            print(
                f"error: Schema not found: {args.schema}",
                file=sys.stderr,
            )
            sys.exit(1)

        with open(schema_path) as f:
            schema = json.load(f)

        errors = validate_tenders(tenders, schema)
        if errors:
            print(f"error: Validation failed: {len(errors)} errors")
            for err in errors:
                print(f"  - {err}")
            sys.exit(1)
        else:
            print(f"success: All {len(tenders)} tenders validated")

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(
                tenders,
                f,
                indent=2 if args.pretty else None,
                ensure_ascii=False,
            )
        print(f"\nsuccess: Saved {len(tenders)} tenders to {args.output}")
    else:
        # Output to stdout
        output = json.dumps(
            tenders,
            indent=2 if args.pretty else None,
            ensure_ascii=False,
        )
        print(output)


if __name__ == "__main__":
    main()
