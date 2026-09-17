import pandas as pd


def prepare_time_series(df):
    """
    Prepare sales data for time-series analysis.
    """

    df = df.copy()

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Sort by date
    df = df.sort_values("date")

    # Set date as index
    df = df.set_index("date")

    return df


def resample_sales(df, frequency="D"):
    """
    Resample sales data.

    D  = Daily
    W  = Weekly
    ME = Monthly
    """

    sales = df["sales"].resample(frequency).sum()

    return sales


def calculate_moving_average(series, window=7):
    """
    Calculate moving average.
    Default = 7 periods.
    """

    return series.rolling(window=window).mean()