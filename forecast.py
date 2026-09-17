import numpy as np
import pandas as pd


def forecast_demand(series, periods=7):
    """
    Forecast future demand using a linear trend.
    """

    series = series.dropna()

    if len(series) < 2:
        raise ValueError("At least 2 data points are required for forecasting.")

    # Create numerical time positions
    X = np.arange(len(series))
    y = series.values

    # Calculate trend line
    slope, intercept = np.polyfit(X, y, 1)

    # Future positions
    future_X = np.arange(
        len(series),
        len(series) + periods
    )

    # Generate predictions
    forecast_values = slope * future_X + intercept

    # Demand cannot be negative
    forecast_values = np.maximum(forecast_values, 0)

    # Generate future dates
    future_dates = pd.date_range(
        start=series.index[-1] + pd.Timedelta(days=1),
        periods=periods,
        freq="D"
    )

    # Create forecast DataFrame
    forecast = pd.DataFrame(
        {
            "forecast_sales": np.round(forecast_values, 2)
        },
        index=future_dates
    )

    return forecast