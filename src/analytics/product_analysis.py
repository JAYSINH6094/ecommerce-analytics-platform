import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


# ============================================================
# LOAD DATA
# ============================================================

sales = pd.read_csv(
    PROCESSED_DATA / "analysis_ready_sales.csv"
)


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

category_analysis = (
    sales
    .groupby("product_category_name_english")
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique"),
        units_sold=("order_item_id", "count"),
        average_price=("price", "mean")
    )
    .reset_index()
)


# ============================================================
# ROUND VALUES
# ============================================================

category_analysis["revenue"] = (
    category_analysis["revenue"].round(2)
)

category_analysis["average_price"] = (
    category_analysis["average_price"].round(2)
)


# ============================================================
# SORT BY REVENUE
# ============================================================

category_analysis = category_analysis.sort_values(
    "revenue",
    ascending=False
)


# ============================================================
# DISPLAY TOP CATEGORIES
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 PRODUCT CATEGORIES BY REVENUE")
print("=" * 70)

print(
    category_analysis
    .head(10)
    .to_string(index=False)
)


# ============================================================
# TOP PRODUCTS BY REVENUE
# ============================================================

product_analysis = (
    sales
    .groupby(
        [
            "product_id",
            "product_category_name_english"
        ]
    )
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique"),
        units_sold=("order_item_id", "count"),
        average_price=("price", "mean")
    )
    .reset_index()
)


product_analysis["revenue"] = (
    product_analysis["revenue"].round(2)
)

product_analysis["average_price"] = (
    product_analysis["average_price"].round(2)
)


product_analysis = product_analysis.sort_values(
    "revenue",
    ascending=False
)


print("\n" + "=" * 70)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 70)

print(
    product_analysis
    .head(10)
    .to_string(index=False)
)


# ============================================================
# CATEGORY REVENUE CHART
# ============================================================

top_categories = category_analysis.head(10)

plt.figure(figsize=(12, 6))

plt.barh(
    top_categories[
        "product_category_name_english"
    ][::-1],
    top_categories["revenue"][::-1]
)

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product Category")

plt.tight_layout()
plt.show()


# ============================================================
# TOP PRODUCTS REVENUE CHART
# ============================================================

top_products = product_analysis.head(10)

plt.figure(figsize=(12, 6))

plt.barh(
    top_products["product_id"][::-1],
    top_products["revenue"][::-1]
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product ID")

plt.tight_layout()
plt.show()


# ============================================================
# SAVE RESULTS
# ============================================================

category_output = (
    PROCESSED_DATA /
    "category_analysis.csv"
)

product_output = (
    PROCESSED_DATA /
    "product_analysis.csv"
)


category_analysis.to_csv(
    category_output,
    index=False
)

product_analysis.to_csv(
    product_output,
    index=False
)


print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(category_output)
print(product_output)

print("\n" + "=" * 70)
print("STEP 7.4 COMPLETED")
print("=" * 70)