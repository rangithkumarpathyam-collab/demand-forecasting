"""Simple JSON-friendly API layer for inventory and replenishment decisions."""

from __future__ import annotations

import json
from typing import Any, Dict

from recommendations import build_recommendation


def recommend_inventory(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Accept a forecast payload and return the final stock recommendation."""
    required_fields = {
        "current_stock",
        "forecasted_demand",
        "lead_time_days",
        "average_demand",
        "demand_std_dev",
    }

    missing = sorted(required_fields - set(payload))
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    return build_recommendation(
        current_stock=float(payload["current_stock"]),
        forecasted_demand=float(payload["forecasted_demand"]),
        lead_time_days=float(payload["lead_time_days"]),
        average_demand=float(payload["average_demand"]),
        demand_std_dev=float(payload["demand_std_dev"]),
        service_level=float(payload.get("service_level", 1.65)),
        target_days_of_stock=float(payload.get("target_days_of_stock", 14)),
        max_inventory=float(payload.get("max_inventory", 0.0)) or None,
    )


def inventory_api(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Public API wrapper for downstream systems and UIs."""
    return recommend_inventory(payload)


if __name__ == "__main__":
    sample = {
        "current_stock": 25,
        "forecasted_demand": 120,
        "lead_time_days": 7,
        "average_demand": 18,
        "demand_std_dev": 8,
        "service_level": 1.65,
        "target_days_of_stock": 14,
        "max_inventory": 250,
    }
    print(json.dumps(inventory_api(sample), indent=2))
