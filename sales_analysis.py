def total_sales(df):
    return df["sales"].sum()


def average_demand(df):
    return df["sales"].mean()


def best_selling_products(df):
    return (
        df.groupby("product_id")["sales"]
        .sum()
        .sort_values(ascending=False)
    )


def sales_by_product(df):
    return (
        df.groupby("product_id")
        .agg(
            total_sales=("sales", "sum"),
            average_sales=("sales", "mean")
        )
        .sort_values(
            by="total_sales",
            ascending=False
        )
    )
def promotion_analysis(df):
    return (
        df.groupby("promotion")["sales"]
        .agg(["sum", "mean", "count"])
    )


def price_analysis(df):
    return (
        df.groupby("price")["sales"]
        .agg(["sum", "mean", "count"])
    )