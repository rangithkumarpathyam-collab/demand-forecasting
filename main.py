from visualization import (
    sales_trend,
    product_sales,
    promotion_sales,
    price_sales
)
from data_loader import load_sales_data

from data_cleaning import (
    clean_sales_data,
    aggregate_daily_sales,
    aggregate_monthly_sales
)

from sales_analysis import (
    total_sales,
    average_demand,
    best_selling_products,
    sales_by_product,
    promotion_analysis,
    price_analysis
)


# 1. Load sales data
df = load_sales_data("sales_data.csv")


# 2. Clean the data
df = clean_sales_data(df)


# 3. Display cleaned data
print("\n===== CLEANED SALES DATA =====")
print(df)


# 4. Historical sales analysis
print("\n===== SALES SUMMARY =====")

print("Total Sales:", total_sales(df))

print("Average Demand:", round(average_demand(df), 2))


# 5. Best-selling products
print("\n===== BEST-SELLING PRODUCTS =====")
print(best_selling_products(df))


# 6. Daily sales
daily = aggregate_daily_sales(df)

print("\n===== DAILY SALES =====")
print(daily)


# 7. Monthly sales
monthly = aggregate_monthly_sales(df)

print("\n===== MONTHLY SALES =====")
print(monthly)


# 8. Product-wise analysis
print("\n===== PRODUCT ANALYSIS =====")
print(sales_by_product(df))


# 9. Promotion analysis
print("\n===== PROMOTION ANALYSIS =====")
print(promotion_analysis(df))


# 10. Price analysis
print("\n===== PRICE ANALYSIS =====")
print(price_analysis(df))


print("\n===== PROGRAM COMPLETED SUCCESSFULLY =====")
print("\n===== GENERATING GRAPHS =====")

sales_trend(df)

product_sales(df)

promotion_sales(df)

price_sales(df)