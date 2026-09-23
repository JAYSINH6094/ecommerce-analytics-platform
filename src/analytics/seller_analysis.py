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

sellers = pd.read_csv(
    PROCESSED_DATA / "sellers.csv"
)


# ============================================================
# SELLER DATA PREPARATION
# ============================================================

sales["revenue"] = pd.to_numeric(
    sales["revenue"],
    errors="coerce"
)

sales["price"] = pd.to_numeric(
    sales["price"],
    errors="coerce"
)

# Keep delivered order items only.
# analysis_ready_sales already contains delivered orders.
seller_sales = sales[
    [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "price",
        "revenue"
    ]
].copy()


# ============================================================
# SELLER PERFORMANCE
# ============================================================

seller_performance = (
    seller_sales
    .groupby("seller_id")
    .agg(
        orders=("order_id", "nunique"),
        units_sold=("order_item_id", "count"),
        total_revenue=("revenue", "sum"),
        average_item_value=("price", "mean"),
        unique_products=("product_id", "nunique")
    )
    .reset_index()
)


seller_performance["revenue_per_order"] = (
    seller_performance["total_revenue"]
    / seller_performance["orders"]
)

seller_performance["units_per_order"] = (
    seller_performance["units_sold"]
    / seller_performance["orders"]
)


# ============================================================
# MERGE SELLER LOCATION
# ============================================================

seller_performance = seller_performance.merge(
    sellers[
        [
            "seller_id",
            "seller_city",
            "seller_state"
        ]
    ],
    on="seller_id",
    how="left"
)


# ============================================================
# ROUND METRICS
# ============================================================

seller_numeric_columns = [
    "total_revenue",
    "average_item_value",
    "revenue_per_order",
    "units_per_order"
]

seller_performance[seller_numeric_columns] = (
    seller_performance[seller_numeric_columns]
    .round(2)
)


# ============================================================
# OVERALL SELLER METRICS
# ============================================================

total_sellers = seller_performance["seller_id"].nunique()

total_seller_revenue = seller_performance[
    "total_revenue"
].sum()

total_seller_orders = seller_performance[
    "orders"
].sum()

total_units_sold = seller_performance[
    "units_sold"
].sum()

average_revenue_per_seller = (
    seller_performance["total_revenue"].mean()
)


print("\n" + "=" * 70)
print("SELLER PERFORMANCE ANALYSIS")
print("=" * 70)

print(f"Active sellers analyzed: {total_sellers:,}")
print(f"Seller order items analyzed: {total_seller_orders:,}")
print(f"Total units sold: {total_units_sold:,}")
print(
    f"Total seller revenue: "
    f"{total_seller_revenue:,.2f}"
)
print(
    f"Average revenue per seller: "
    f"{average_revenue_per_seller:,.2f}"
)


# ============================================================
# TOP 20 SELLERS
# ============================================================

top_sellers = (
    seller_performance
    .sort_values("total_revenue", ascending=False)
    .head(20)
    .copy()
)

print("\n" + "=" * 70)
print("TOP 20 SELLERS BY REVENUE")
print("=" * 70)

print(
    top_sellers[
        [
            "seller_id",
            "seller_city",
            "seller_state",
            "orders",
            "units_sold",
            "unique_products",
            "total_revenue",
            "average_item_value",
            "revenue_per_order"
        ]
    ].to_string(index=False)
)


# ============================================================
# SELLER STATE ANALYSIS
# ============================================================

state_seller_analysis = (
    seller_performance
    .groupby("seller_state")
    .agg(
        sellers=("seller_id", "nunique"),
        orders=("orders", "sum"),
        units_sold=("units_sold", "sum"),
        total_revenue=("total_revenue", "sum"),
        average_seller_revenue=("total_revenue", "mean"),
        average_item_value=("average_item_value", "mean")
    )
    .reset_index()
)


state_seller_analysis["revenue_percentage"] = (
    state_seller_analysis["total_revenue"]
    / total_seller_revenue
    * 100
)

state_seller_analysis[
    [
        "total_revenue",
        "average_seller_revenue",
        "average_item_value",
        "revenue_percentage"
    ]
] = state_seller_analysis[
    [
        "total_revenue",
        "average_seller_revenue",
        "average_item_value",
        "revenue_percentage"
    ]
].round(2)

state_seller_analysis = state_seller_analysis.sort_values(
    "total_revenue",
    ascending=False
)


print("\n" + "=" * 70)
print("SELLER PERFORMANCE BY STATE")
print("=" * 70)

print(
    state_seller_analysis.head(15)
    .to_string(index=False)
)


# ============================================================
# SELLER REVENUE CONCENTRATION
# ============================================================

seller_ranked = seller_performance.sort_values(
    "total_revenue",
    ascending=False
).copy()

seller_ranked["cumulative_revenue"] = (
    seller_ranked["total_revenue"].cumsum()
)

seller_ranked["cumulative_revenue_percentage"] = (
    seller_ranked["cumulative_revenue"]
    / total_seller_revenue
    * 100
)


top_10_percent_sellers = max(
    1,
    int(total_sellers * 0.10)
)

top_10_percent_seller_revenue = (
    seller_ranked
    .head(top_10_percent_sellers)["total_revenue"]
    .sum()
)

top_10_percent_seller_revenue_percentage = (
    top_10_percent_seller_revenue
    / total_seller_revenue
    * 100
)


print("\n" + "=" * 70)
print("SELLER REVENUE CONCENTRATION")
print("=" * 70)

print(
    f"Top 10% sellers revenue: "
    f"{top_10_percent_seller_revenue:,.2f}"
)

print(
    f"Top 10% seller revenue contribution: "
    f"{top_10_percent_seller_revenue_percentage:.2f}%"
)


# ============================================================
# TOP SELLER INSIGHT
# ============================================================

top_seller = seller_performance.loc[
    seller_performance["total_revenue"].idxmax()
]

highest_volume_seller = seller_performance.loc[
    seller_performance["units_sold"].idxmax()
]

highest_order_seller = seller_performance.loc[
    seller_performance["orders"].idxmax()
]


print("\n" + "=" * 70)
print("KEY SELLER INSIGHTS")
print("=" * 70)

print(
    f"Highest revenue seller: "
    f"{top_seller['seller_id']}"
)

print(
    f"Highest revenue seller value: "
    f"{top_seller['total_revenue']:,.2f}"
)

print(
    f"Highest unit-volume seller: "
    f"{highest_volume_seller['seller_id']}"
)

print(
    f"Highest order-volume seller: "
    f"{highest_order_seller['seller_id']}"
)


# ============================================================
# CHART 1: TOP 10 SELLERS BY REVENUE
# ============================================================

top_10_chart = (
    seller_performance
    .sort_values("total_revenue", ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

plt.bar(
    top_10_chart["seller_id"].astype(str),
    top_10_chart["total_revenue"]
)

plt.title("Top 10 Sellers by Revenue")
plt.xlabel("Seller ID")
plt.ylabel("Total Revenue")

plt.xticks(rotation=75)
plt.tight_layout()

plt.show()


# ============================================================
# CHART 2: SELLER REVENUE BY STATE
# ============================================================

top_states_chart = (
    state_seller_analysis
    .head(10)
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_states_chart["seller_state"],
    top_states_chart["total_revenue"]
)

plt.title("Seller Revenue by State")
plt.xlabel("Seller State")
plt.ylabel("Total Revenue")

plt.tight_layout()

plt.show()


# ============================================================
# SAVE RESULTS
# ============================================================

seller_performance.to_csv(
    PROCESSED_DATA / "seller_analysis.csv",
    index=False
)

state_seller_analysis.to_csv(
    PROCESSED_DATA / "state_seller_analysis.csv",
    index=False
)

top_sellers.to_csv(
    PROCESSED_DATA / "top_sellers.csv",
    index=False
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(
    PROCESSED_DATA / "seller_analysis.csv"
)

print(
    PROCESSED_DATA / "state_seller_analysis.csv"
)

print(
    PROCESSED_DATA / "top_sellers.csv"
)

print("\n" + "=" * 70)
print("STEP 7.14 COMPLETED")
print("=" * 70)