import matplotlib.pyplot as plt


def sales_trend(df):
    daily_sales = (
        df.groupby("date")["sales"]
        .sum()
        .reset_index()
    )

    plt.figure(figsize=(10, 5))
    plt.plot(
        daily_sales["date"],
        daily_sales["sales"],
        marker="o"
    )

    plt.title("Sales Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Units Sold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def product_sales(df):
    product_sales = (
        df.groupby("product_id")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    product_sales.plot(kind="bar")

    plt.title("Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Units Sold")
    plt.tight_layout()
    plt.show()


def promotion_sales(df):
    promotion_sales = (
        df.groupby("promotion")["sales"]
        .mean()
    )

    plt.figure(figsize=(8, 5))
    promotion_sales.plot(kind="bar")

    plt.title("Average Sales: Promotion vs No Promotion")
    plt.xlabel("Promotion (0 = No, 1 = Yes)")
    
    plt.ylabel("Average Units Sold")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def price_sales(df):
    price_sales = (
        df.groupby("price")["sales"]
        .mean()
    )

    plt.figure(figsize=(8, 5))
    price_sales.plot(kind="bar")

    plt.title("Average Sales by Price")
    plt.xlabel("Price")
    plt.ylabel("Average Units Sold")
    plt.tight_layout()
    plt.show()