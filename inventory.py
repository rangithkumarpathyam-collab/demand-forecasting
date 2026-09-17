"""Inventory math for demand forecasting and stock decisions."""

from __future__ import annotations

import math


def calculate_safety_stock(
    average_demand: float,
    demand_std_dev: float,
    lead_time_days: float,
    service_level: float = 1.65,
) -> float:
    """Calculate safety stock using a service-level factor and lead-time demand volatility."""
    average_demand = float(average_demand)
    demand_std_dev = float(demand_std_dev)
    lead_time_days = float(lead_time_days)
    service_level = float(service_level)

    if average_demand < 0:
        raise ValueError("average_demand must be non-negative")
    if demand_std_dev < 0:
        raise ValueError("demand_std_dev must be non-negative")
    if lead_time_days <= 0:
        raise ValueError("lead_time_days must be greater than zero")
    if service_level <= 0:
        raise ValueError("service_level must be greater than zero")

    safety_stock = demand_std_dev * math.sqrt(lead_time_days) * service_level
    return max(0.0, safety_stock)


def calculate_reorder_point(
    avg_daily_demand: float,
    lead_time_days: float,
    safety_stock: float,
) -> float:
    """Return the reorder point for replenishment planning."""
    avg_daily_demand = float(avg_daily_demand)
    lead_time_days = float(lead_time_days)
    safety_stock = float(safety_stock)

    if avg_daily_demand < 0:
        raise ValueError("avg_daily_demand must be non-negative")
    if lead_time_days <= 0:
        raise ValueError("lead_time_days must be greater than zero")

    reorder_point = (avg_daily_demand * lead_time_days) + safety_stock
    return max(0.0, reorder_point)


def assess_stockout_risk(current_stock: float, reorder_point: float) -> str:
    """Classify the risk of running out of inventory before replenishment."""
    current_stock = float(current_stock)
    reorder_point = float(reorder_point)

    if reorder_point <= 0:
        return "low"

    ratio = current_stock / reorder_point
    if ratio <= 0.5:
        return "high"
    if ratio <= 0.9:
        return "medium"
    return "low"


def assess_overstock_risk(current_stock: float, target_stock: float, max_inventory: float) -> str:
    """Classify whether the current inventory is above a healthy threshold."""
    current_stock = float(current_stock)
    target_stock = float(target_stock)
    max_inventory = float(max_inventory)

    if max_inventory <= 0:
        return "low"
    if current_stock >= max_inventory:
        return "high"
    if current_stock > target_stock:
        return "medium"
    return "low"
