import pandas as pd

from src.time_series import (
    prepare_time_series,
    resample_sales,
    calculate_moving_average
)

from src.trend_seasonality import (
    detect_trend,
    detect_weekly_seasonality
)

from src.anomaly_detection import (
    detect_anomalies
)

from src.forecast import forecast_demand

from src.visualization import plot_forecast

# Load data
df = pd.read_csv("data/sales.csv")

print("=" * 50)
print("DEMAND FORECASTING SYSTEM")
print("=" * 50)

# Prepare time series
df = prepare_time_series(df)

print("\nPrepared Data:")
print(df)

# Daily sales
daily_sales = resample_sales(df, "D")

print("\nDaily Sales:")
print(daily_sales)

# Weekly sales
weekly_sales = resample_sales(df, "W")

print("\nWeekly Sales:")
print(weekly_sales)

# Moving average
moving_average = calculate_moving_average(daily_sales, window=7)

print("\n7-Day Moving Average:")
print(moving_average)

# Trend detection
trend_result = detect_trend(daily_sales)

print("\nTrend Result:")
print(trend_result)

# Seasonality detection
seasonality_result = detect_weekly_seasonality(daily_sales)

print("\nSeasonality Result:")
print(seasonality_result)

# Anomaly detection
anomaly_result = detect_anomalies(daily_sales)

print("\nAnomaly Detection:")
print(anomaly_result)

# Demand forecasting
forecast = forecast_demand(daily_sales, periods=7)

print("\n7-Day Demand Forecast:")
print(forecast)

print("\nForecast Summary:")
print(f"Average predicted demand: {forecast['forecast_sales'].mean():.2f}")
print(f"Minimum predicted demand: {forecast['forecast_sales'].min():.2f}")
print(f"Maximum predicted demand: {forecast['forecast_sales'].max():.2f}")

# Visualize forecast
plot_forecast(daily_sales, forecast)

print("\n" + "=" * 50)
print("ANALYSIS COMPLETE")
print("=" * 50)
