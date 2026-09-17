import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.time_series import (
    prepare_time_series,
    resample_sales,
    calculate_moving_average
)

from src.trend_seasonality import (
    detect_trend,
    detect_weekly_seasonality
)

from src.anomaly_detection import detect_anomalies
from src.forecast import forecast_demand


st.set_page_config(
    page_title="Demand Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Demand Forecasting System")
st.write("Analyze historical sales and predict future demand.")
st.divider()
# Load data
uploaded_file = st.file_uploader(
    "Upload your sales CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

else:

    df = pd.read_csv("data/sales.csv")


# Prepare data
df = prepare_time_series(df)

# Daily sales
daily_sales = resample_sales(df, "D")

# Trend
trend_result = detect_trend(daily_sales)

# Seasonality
seasonality_result = detect_weekly_seasonality(daily_sales)

# Anomalies
anomaly_result = detect_anomalies(daily_sales)

# Forecast
forecast = forecast_demand(daily_sales, periods=7)

st.subheader("📊 Forecast Summary")
col1, col2, col3 = st.columns(3)

col1.metric("Average Demand", f"{forecast['forecast_sales'].mean():.2f}")
col2.metric("Minimum Demand", f"{forecast['forecast_sales'].min():.2f}")
col3.metric("Maximum Demand", f"{forecast['forecast_sales'].max():.2f}")

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Trend",
        trend_result["trend"].title()
    )

with col2:
    st.metric(
        "Seasonality",
        seasonality_result["strength"].title()
    )

with col3:
    st.metric(
        "Average Forecast",
        f"{forecast['forecast_sales'].mean():.2f}"
    )


st.subheader("Demand History & Forecast")

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    daily_sales.index,
    daily_sales.values,
    marker="o",
    label="Historical Sales"
)

ax.plot(
    forecast.index,
    forecast["forecast_sales"],
    marker="o",
    linestyle="--",
    label="Forecast"
)

ax.set_title("Demand Forecast")
ax.set_xlabel("Date")
ax.set_ylabel("Sales")
ax.legend()
ax.grid(True)

fig.tight_layout()

st.subheader("📈 7-Day Demand Forecast")
st.pyplot(fig)
plt.close(fig)
st.divider()


st.subheader("Anomaly Detection")

st.text(anomaly_result.to_string())


st.subheader("Forecast Values")

st.text(forecast.to_string())