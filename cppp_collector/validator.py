"""
Schema validation for normalized procurement data
"""

from __future__ import annotations

from typing import Any

import jsonschema


def validate_tenders(
    tenders: list[dict[str, Any]], schema: dict[str, Any]
) -> list[str]:
    """
    Validate tenders against schema

    Args:
        tenders: List of tender records to validate
        schema: JSON schema dict

    Returns:
        List of error messages (empty if valid)
    """
    errors: list[str] = []

    for i, tender in enumerate(tenders):
        try:
            jsonschema.validate(tender, schema)
        except jsonschema.ValidationError as e:
            tender_id = tender.get("identity", {}).get("tender_id", f"[index {i}]")
            errors.append(f"{tender_id}: {e.message}")

    return errors


def validate_tender(tender: dict[str, Any], schema: dict[str, Any]) -> bool:
    """
    Validate a single tender against schema

    Args:
        tender: Tender record to validate
        schema: JSON schema dict

    Returns:
        True if valid, False otherwise
    """
    try:
        jsonschema.validate(tender, schema)
        return True
    except jsonschema.ValidationError:
        return False
