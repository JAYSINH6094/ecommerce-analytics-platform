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
# REGIONAL ANALYSIS
# ============================================================

regional_analysis = (
    sales
    .groupby("customer_state")
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique"),
        customers=("customer_unique_id", "nunique"),
        units_sold=("order_item_id", "count")
    )
    .reset_index()
)


# ============================================================
# AVERAGE ORDER VALUE
# ============================================================

regional_analysis["aov"] = (
    regional_analysis["revenue"]
    / regional_analysis["orders"]
)


# ============================================================
# ROUND VALUES
# ============================================================

regional_analysis["revenue"] = (
    regional_analysis["revenue"].round(2)
)

regional_analysis["aov"] = (
    regional_analysis["aov"].round(2)
)


# ============================================================
# SORT BY REVENUE
# ============================================================

regional_analysis = regional_analysis.sort_values(
    "revenue",
    ascending=False
)


# ============================================================
# TOP 10 STATES BY REVENUE
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 STATES BY REVENUE")
print("=" * 70)

print(
    regional_analysis
    .head(10)
    .to_string(index=False)
)


# ============================================================
# TOP 10 STATES BY ORDERS
# ============================================================

top_orders = (
    regional_analysis
    .sort_values(
        "orders",
        ascending=False
    )
    .head(10)
)


print("\n" + "=" * 70)
print("TOP 10 STATES BY ORDERS")
print("=" * 70)

print(
    top_orders.to_string(index=False)
)


# ============================================================
# REGIONAL SUMMARY
# ============================================================

highest_revenue_state = regional_analysis.iloc[0]

highest_order_state = (
    regional_analysis
    .sort_values(
        "orders",
        ascending=False
    )
    .iloc[0]
)


print("\n" + "=" * 70)
print("REGIONAL BUSINESS INSIGHTS")
print("=" * 70)

print(
    f"Highest revenue state: "
    f"{highest_revenue_state['customer_state']} "
    f"({highest_revenue_state['revenue']:,.2f})"
)

print(
    f"Highest order-volume state: "
    f"{highest_order_state['customer_state']} "
    f"({highest_order_state['orders']:,} orders)"
)


# ============================================================
# REVENUE BY STATE CHART
# ============================================================

top_revenue_states = (
    regional_analysis
    .head(10)
)

plt.figure(figsize=(12, 6))

plt.barh(
    top_revenue_states["customer_state"][::-1],
    top_revenue_states["revenue"][::-1]
)

plt.title("Top 10 States by Revenue")
plt.xlabel("Revenue")
plt.ylabel("State")

plt.tight_layout()
plt.show()


# ============================================================
# ORDERS BY STATE CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.barh(
    top_orders["customer_state"][::-1],
    top_orders["orders"][::-1]
)

plt.title("Top 10 States by Orders")
plt.xlabel("Number of Orders")
plt.ylabel("State")

plt.tight_layout()
plt.show()


# ============================================================
# SAVE REGIONAL ANALYSIS
# ============================================================

OUTPUT_FILE = (
    PROCESSED_DATA /
    "regional_analysis.csv"
)

regional_analysis.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved regional analysis to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("STEP 7.6 COMPLETED")
print("=" * 70)