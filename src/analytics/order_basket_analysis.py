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
# BASIC CLEANING
# ============================================================

sales["revenue"] = pd.to_numeric(
    sales["revenue"],
    errors="coerce"
)

sales["price"] = pd.to_numeric(
    sales["price"],
    errors="coerce"
)


# ============================================================
# ORDER-LEVEL BASKET ANALYSIS
# ============================================================

order_baskets = (
    sales
    .groupby("order_id")
    .agg(
        customer_id=("customer_unique_id", "first"),
        item_count=("order_item_id", "count"),
        unique_products=("product_id", "nunique"),
        basket_revenue=("revenue", "sum"),
        average_item_price=("price", "mean")
    )
    .reset_index()
)


# ============================================================
# BASKET TYPE
# ============================================================

order_baskets["basket_type"] = order_baskets[
    "item_count"
].apply(
    lambda x: "Single-Item Order"
    if x == 1
    else "Multi-Item Order"
)


# ============================================================
# ORDER-LEVEL METRICS
# ============================================================

total_orders = len(order_baskets)

total_items = order_baskets["item_count"].sum()

total_revenue = order_baskets["basket_revenue"].sum()

average_items_per_order = (
    order_baskets["item_count"].mean()
)

median_items_per_order = (
    order_baskets["item_count"].median()
)

average_basket_value = (
    order_baskets["basket_revenue"].mean()
)

median_basket_value = (
    order_baskets["basket_revenue"].median()
)

maximum_basket_value = (
    order_baskets["basket_revenue"].max()
)

maximum_basket_items = (
    order_baskets["item_count"].max()
)


print("\n" + "=" * 70)
print("ORDER & BASKET ANALYSIS")
print("=" * 70)

print(f"Orders analyzed: {total_orders:,}")
print(f"Total items sold: {total_items:,}")
print(
    f"Average items per order: "
    f"{average_items_per_order:.2f}"
)
print(
    f"Median items per order: "
    f"{median_items_per_order:.2f}"
)
print(
    f"Average basket value: "
    f"{average_basket_value:,.2f}"
)
print(
    f"Median basket value: "
    f"{median_basket_value:,.2f}"
)
print(
    f"Maximum basket value: "
    f"{maximum_basket_value:,.2f}"
)
print(
    f"Maximum items in a single order: "
    f"{maximum_basket_items:,}"
)


# ============================================================
# SINGLE VS MULTI-ITEM ORDERS
# ============================================================

basket_type_analysis = (
    order_baskets
    .groupby("basket_type")
    .agg(
        orders=("order_id", "count"),
        total_items=("item_count", "sum"),
        total_revenue=("basket_revenue", "sum"),
        average_basket_value=("basket_revenue", "mean"),
        average_items_per_order=("item_count", "mean")
    )
    .reset_index()
)


basket_type_analysis["order_percentage"] = (
    basket_type_analysis["orders"]
    / total_orders
    * 100
)

basket_type_analysis["revenue_percentage"] = (
    basket_type_analysis["total_revenue"]
    / total_revenue
    * 100
)


basket_numeric_columns = [
    "total_revenue",
    "average_basket_value",
    "average_items_per_order",
    "order_percentage",
    "revenue_percentage"
]

basket_type_analysis[basket_numeric_columns] = (
    basket_type_analysis[basket_numeric_columns]
    .round(2)
)


print("\n" + "=" * 70)
print("SINGLE VS MULTI-ITEM ORDERS")
print("=" * 70)

print(
    basket_type_analysis.to_string(index=False)
)


# ============================================================
# BASKET SIZE DISTRIBUTION
# ============================================================

def basket_size_group(item_count):
    if item_count == 1:
        return "1 Item"
    elif item_count == 2:
        return "2 Items"
    elif item_count == 3:
        return "3 Items"
    elif item_count == 4:
        return "4 Items"
    else:
        return "5+ Items"


order_baskets["basket_size_group"] = (
    order_baskets["item_count"]
    .apply(basket_size_group)
)


basket_size_analysis = (
    order_baskets
    .groupby("basket_size_group")
    .agg(
        orders=("order_id", "count"),
        total_items=("item_count", "sum"),
        total_revenue=("basket_revenue", "sum"),
        average_basket_value=("basket_revenue", "mean")
    )
    .reset_index()
)


basket_size_analysis["order_percentage"] = (
    basket_size_analysis["orders"]
    / total_orders
    * 100
)

basket_size_analysis["revenue_percentage"] = (
    basket_size_analysis["total_revenue"]
    / total_revenue
    * 100
)


basket_size_numeric_columns = [
    "total_revenue",
    "average_basket_value",
    "order_percentage",
    "revenue_percentage"
]

basket_size_analysis[basket_size_numeric_columns] = (
    basket_size_analysis[basket_size_numeric_columns]
    .round(2)
)


basket_size_order = [
    "1 Item",
    "2 Items",
    "3 Items",
    "4 Items",
    "5+ Items"
]

basket_size_analysis["basket_size_group"] = pd.Categorical(
    basket_size_analysis["basket_size_group"],
    categories=basket_size_order,
    ordered=True
)

basket_size_analysis = basket_size_analysis.sort_values(
    "basket_size_group"
)


print("\n" + "=" * 70)
print("BASKET SIZE DISTRIBUTION")
print("=" * 70)

print(
    basket_size_analysis.to_string(index=False)
)


# ============================================================
# HIGH-VALUE ORDERS
# ============================================================

high_value_orders = (
    order_baskets
    .sort_values("basket_revenue", ascending=False)
    .head(20)
    .copy()
)


high_value_orders[
    [
        "basket_revenue",
        "average_item_price"
    ]
] = high_value_orders[
    [
        "basket_revenue",
        "average_item_price"
    ]
].round(2)


print("\n" + "=" * 70)
print("TOP 20 HIGH-VALUE ORDERS")
print("=" * 70)

print(
    high_value_orders[
        [
            "order_id",
            "customer_id",
            "item_count",
            "unique_products",
            "basket_revenue",
            "average_item_price",
            "basket_type"
        ]
    ].to_string(index=False)
)


# ============================================================
# BASKET SIZE VS REVENUE
# ============================================================

basket_relationship = (
    order_baskets
    .groupby("item_count")
    .agg(
        orders=("order_id", "count"),
        average_basket_value=("basket_revenue", "mean"),
        median_basket_value=("basket_revenue", "median"),
        total_revenue=("basket_revenue", "sum")
    )
    .reset_index()
)


basket_relationship[
    [
        "average_basket_value",
        "median_basket_value",
        "total_revenue"
    ]
] = basket_relationship[
    [
        "average_basket_value",
        "median_basket_value",
        "total_revenue"
    ]
].round(2)


print("\n" + "=" * 70)
print("BASKET SIZE VS REVENUE")
print("=" * 70)

print(
    basket_relationship.head(15)
    .to_string(index=False)
)


# ============================================================
# KEY BUSINESS INSIGHTS
# ============================================================

largest_basket_group = basket_size_analysis.loc[
    basket_size_analysis["orders"].idxmax()
]

highest_revenue_basket_group = basket_size_analysis.loc[
    basket_size_analysis["total_revenue"].idxmax()
]

highest_average_basket_group = basket_size_analysis.loc[
    basket_size_analysis["average_basket_value"].idxmax()
]


print("\n" + "=" * 70)
print("KEY BASKET INSIGHTS")
print("=" * 70)

print(
    f"Most common basket size: "
    f"{largest_basket_group['basket_size_group']}"
)

print(
    f"Largest revenue basket-size group: "
    f"{highest_revenue_basket_group['basket_size_group']}"
)

print(
    f"Highest average basket value group: "
    f"{highest_average_basket_group['basket_size_group']}"
)


# ============================================================
# CHART 1: SINGLE VS MULTI-ITEM
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    basket_type_analysis["basket_type"],
    basket_type_analysis["orders"]
)

plt.title("Single-Item vs Multi-Item Orders")
plt.xlabel("Basket Type")
plt.ylabel("Number of Orders")

plt.xticks(rotation=15)
plt.tight_layout()

plt.show()


# ============================================================
# CHART 2: BASKET SIZE REVENUE
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    basket_size_analysis["basket_size_group"].astype(str),
    basket_size_analysis["total_revenue"]
)

plt.title("Revenue by Basket Size")
plt.xlabel("Basket Size")
plt.ylabel("Total Revenue")

plt.tight_layout()

plt.show()


# ============================================================
# SAVE RESULTS
# ============================================================

order_baskets.to_csv(
    PROCESSED_DATA / "order_basket_analysis.csv",
    index=False
)

basket_type_analysis.to_csv(
    PROCESSED_DATA / "basket_type_analysis.csv",
    index=False
)

basket_size_analysis.to_csv(
    PROCESSED_DATA / "basket_size_analysis.csv",
    index=False
)

basket_relationship.to_csv(
    PROCESSED_DATA / "basket_size_revenue_analysis.csv",
    index=False
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(
    PROCESSED_DATA / "order_basket_analysis.csv"
)

print(
    PROCESSED_DATA / "basket_type_analysis.csv"
)

print(
    PROCESSED_DATA / "basket_size_analysis.csv"
)

print(
    PROCESSED_DATA / "basket_size_revenue_analysis.csv"
)

print("\n" + "=" * 70)
print("STEP 7.15 COMPLETED")
print("=" * 70)