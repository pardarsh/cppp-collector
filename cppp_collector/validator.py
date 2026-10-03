"""
Schema validation for normalized procurement data
"""

from typing import Any, Dict, List

import jsonschema


def validate_tenders(
    tenders: List[Dict[str, Any]], schema: Dict[str, Any]
) -> List[str]:
    """
    Validate tenders against schema

    Args:
        tenders: List of tender records to validate
        schema: JSON schema dict

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    for i, tender in enumerate(tenders):
        try:
            jsonschema.validate(tender, schema)
        except jsonschema.ValidationError as e:
            tender_id = tender.get("identity", {}).get("tender_id", f"[index {i}]")
            errors.append(f"{tender_id}: {e.message}")

    return errors


def validate_tender(tender: Dict[str, Any], schema: Dict[str, Any]) -> bool:
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
