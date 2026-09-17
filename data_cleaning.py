import pandas as pd


def clean_sales_data(df):
    df = df.copy()

    # Convert date
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Convert numeric columns
    df["sales"] = pd.to_numeric(
        df["sales"],
        errors="coerce"
    )

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    df["promotion"] = pd.to_numeric(
        df["promotion"],
        errors="coerce"
    )

    # Remove missing values
    df = df.dropna(
        subset=[
            "date",
            "product_id",
            "sales",
            "price",
            "promotion"
        ]
    )

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove invalid values
    df = df[
        (df["sales"] >= 0) &
        (df["price"] >= 0) &
        (df["promotion"].isin([0, 1]))
    ]

    return df


def aggregate_daily_sales(df):
    daily_sales = (
        df.groupby(["date", "product_id"])["sales"]
        .sum()
        .reset_index()
    )

    return daily_sales


def aggregate_monthly_sales(df):
    df = df.copy()

    df["month"] = df["date"].dt.to_period("M")

    monthly_sales = (
        df.groupby(["month", "product_id"])["sales"]
        .sum()
        .reset_index()
    )

    return monthly_sales