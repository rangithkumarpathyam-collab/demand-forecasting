import pandas as pd


def detect_anomalies(series, window=7, threshold=2):
    """
    Detect unusually high or low sales using a rolling mean
    and rolling standard deviation.
    """

    series = series.dropna()

    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()

    upper_limit = rolling_mean + threshold * rolling_std
    lower_limit = rolling_mean - threshold * rolling_std

    anomalies = (series > upper_limit) | (series < lower_limit)

    result = pd.DataFrame({
        "sales": series,
        "rolling_mean": rolling_mean,
        "upper_limit": upper_limit,
        "lower_limit": lower_limit,
        "anomaly": anomalies
    })

    return result


if __name__ == "__main__":

    # Load sales data
    df = pd.read_csv("data/sales.csv")

    # Prepare dates
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df = df.set_index("date")

    # Create daily sales
    daily_sales = df["sales"].resample("D").sum()

    # Detect anomalies
    result = detect_anomalies(daily_sales)

    print("Anomaly Detection Result:")
    print(result)