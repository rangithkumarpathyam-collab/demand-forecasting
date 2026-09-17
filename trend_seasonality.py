import numpy as np


def detect_trend(series):
    """
    Detect whether sales are increasing, decreasing, or stable.
    """

    # Remove missing values
    series = series.dropna()

    # Create time positions
    X = np.arange(len(series))

    # Sales values
    y = series.values

    # Calculate trend slope
    slope = np.polyfit(X, y, 1)[0]

    # Normalize slope
    mean_sales = series.mean()

    if mean_sales != 0:
        normalized_slope = slope / mean_sales
    else:
        normalized_slope = 0

    # Classify trend
    if normalized_slope > 0.01:
        trend = "increasing"
    elif normalized_slope < -0.01:
        trend = "decreasing"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "slope": slope,
        "normalized_slope": normalized_slope
    }


def detect_weekly_seasonality(series):
    """
    Detect weekly seasonality using autocorrelation.
    """

    series = series.dropna()

    # Need more than 7 data points
    if len(series) <= 7:
        return {
            "detected": False,
            "strength": "insufficient data",
            "correlation": None
        }

    correlation = series.autocorr(lag=7)

    if correlation >= 0.7:
        strength = "strong"
        detected = True

    elif correlation >= 0.4:
        strength = "moderate"
        detected = True

    else:
        strength = "weak"
        detected = False

    return {
        "detected": detected,
        "strength": strength,
        "correlation": correlation
    }


# Test the functions
if __name__ == "__main__":
    import pandas as pd

    # Load sales data
    df = pd.read_csv("data/sales.csv")

    # Prepare dates
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df = df.set_index("date")

    # Create daily sales
    daily_sales = df["sales"].resample("D").sum()

    # Detect trend
    trend_result = detect_trend(daily_sales)

    # Detect weekly seasonality
    seasonality_result = detect_weekly_seasonality(daily_sales)

    print("Trend Result:")
    print(trend_result)

    print("\nSeasonality Result:")
    print(seasonality_result)