"""Recommendation layer that turns forecast metrics into replenishment decisions."""

from __future__ import annotations

from typing import Iterable, List

from inventory import (
    assess_overstock_risk,
    assess_stockout_risk,
    calculate_reorder_point,
    calculate_safety_stock,
)


def detect_trend(history: Iterable[float]) -> str:
    """Identify whether recent demand is moving upward, downward, or stable."""
    values = [float(value) for value in history]
    if len(values) < 2:
        return "stable"

    mean = sum(values) / len(values)
    if mean == 0:
        return "stable"

    delta = values[-1] - values[0]
    if delta > 0.1 * mean:
        return "upward"
    if delta < -0.1 * mean:
        return "downward"
    return "stable"


def detect_seasonality(history: Iterable[float], period: int = 7) -> str:
    """Check if demand contains a recurring seasonal pattern."""
    values = [float(value) for value in history]
    if len(values) < period * 2:
        return "low"

    mean = sum(values) / len(values)
    if mean == 0:
        return "low"

    seasonal_amplitude = max(values) - min(values)
    if seasonal_amplitude / mean > 0.15:
        return "present"
    return "low"


def detect_anomalies(history: Iterable[float], threshold: float = 3.0) -> List[int]:
    """Return indexes of points deviating strongly from the historical mean."""
    values = [float(value) for value in history]
    if len(values) < 3:
        return []

    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    std_dev = variance ** 0.5
    if std_dev == 0:
        return []

    anomalies = [idx for idx, value in enumerate(values) if abs(value - mean) > threshold * std_dev]
    return anomalies


def analyze_historical_sales(history: Iterable[float], period: int = 7) -> dict:
    """Summarize historical demand and key forecasting patterns."""
    values = [float(value) for value in history]
    if not values:
        return {
            "mean_demand": 0.0,
            "std_dev_demand": 0.0,
            "trend": "stable",
            "seasonality": "low",
            "anomaly_count": 0,
            "anomalies": [],
        }

    mean_demand = sum(values) / len(values)
    variance = sum((value - mean_demand) ** 2 for value in values) / len(values)
    std_dev_demand = variance ** 0.5

    return {
        "mean_demand": mean_demand,
        "std_dev_demand": std_dev_demand,
        "trend": detect_trend(values),
        "seasonality": detect_seasonality(values, period=period),
        "anomaly_count": len(detect_anomalies(values)),
        "anomalies": detect_anomalies(values),
    }


def build_recommendation(
    current_stock: float,
    forecasted_demand: float,
    lead_time_days: float,
    average_demand: float,
    demand_std_dev: float,
    service_level: float = 1.65,
    target_days_of_stock: float = 14,
    max_inventory: float | None = None,
) -> dict:
    """Convert forecast, lead time, and risk information into stock recommendations."""
    current_stock = float(current_stock)
    forecasted_demand = float(forecasted_demand)
    lead_time_days = float(lead_time_days)
    average_demand = float(average_demand)
    demand_std_dev = float(demand_std_dev)
    service_level = float(service_level)
    target_days_of_stock = float(target_days_of_stock)

    if lead_time_days <= 0:
        raise ValueError("lead_time_days must be greater than zero")

    safety_stock = calculate_safety_stock(
        average_demand=average_demand,
        demand_std_dev=demand_std_dev,
        lead_time_days=lead_time_days,
        service_level=service_level,
    )

    reorder_point = calculate_reorder_point(
        avg_daily_demand=average_demand,
        lead_time_days=lead_time_days,
        safety_stock=safety_stock,
    )

    target_stock = max(average_demand * target_days_of_stock, reorder_point)
    stockout_risk = assess_stockout_risk(current_stock, reorder_point)

    if max_inventory is None:
        max_inventory = target_stock * 2.0
    max_inventory = float(max_inventory)
    overstock_risk = assess_overstock_risk(current_stock, target_stock, max_inventory)

    shortage_gap = max(0.0, reorder_point - current_stock)
    demand_gap = max(0.0, forecasted_demand - current_stock)
    recommended_order_quantity = shortage_gap + demand_gap

    if max_inventory > 0:
        recommended_order_quantity = min(recommended_order_quantity, max(0.0, max_inventory - current_stock))

    if current_stock >= target_stock and stockout_risk == "low":
        recommended_order_quantity = 0.0

    return {
        "reorder_point": reorder_point,
        "safety_stock": safety_stock,
        "stockout_risk": stockout_risk,
        "overstock_risk": overstock_risk,
        "target_stock": target_stock,
        "recommended_order_quantity": max(0.0, recommended_order_quantity),
        "forecasted_demand": forecasted_demand,
        "days_of_cover": (current_stock / max(average_demand, 1.0)) if average_demand > 0 else 0.0,
    }
