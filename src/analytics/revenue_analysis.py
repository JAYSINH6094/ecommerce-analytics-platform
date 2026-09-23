import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


# ============================================================
# LOAD ANALYSIS-READY DATA
# ============================================================

sales = pd.read_csv(
    PROCESSED_DATA / "analysis_ready_sales.csv"
)


# ============================================================
# CONVERT DATE
# ============================================================

sales["order_purchase_timestamp"] = pd.to_datetime(
    sales["order_purchase_timestamp"]
)


# ============================================================
# MONTHLY REVENUE & ORDERS
# ============================================================

monthly_sales = (
    sales
    .groupby("order_month")
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)


# ============================================================
# AVERAGE ORDER VALUE
# ============================================================

monthly_sales["aov"] = (
    monthly_sales["revenue"] /
    monthly_sales["orders"]
)


# ============================================================
# MONTH-OVER-MONTH GROWTH
# ============================================================

monthly_sales["previous_month_revenue"] = (
    monthly_sales["revenue"].shift(1)
)

monthly_sales["mom_growth_percentage"] = (
    (
        monthly_sales["revenue"]
        - monthly_sales["previous_month_revenue"]
    )
    / monthly_sales["previous_month_revenue"]
) * 100


# ============================================================
# ROUND VALUES
# ============================================================

monthly_sales["revenue"] = monthly_sales["revenue"].round(2)
monthly_sales["aov"] = monthly_sales["aov"].round(2)
monthly_sales["mom_growth_percentage"] = (
    monthly_sales["mom_growth_percentage"].round(2)
)


# ============================================================
# DISPLAY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MONTHLY SALES ANALYSIS")
print("=" * 70)

print(monthly_sales.to_string(index=False))


# ============================================================
# KEY METRICS
# ============================================================

highest_revenue_month = monthly_sales.loc[
    monthly_sales["revenue"].idxmax()
]

highest_order_month = monthly_sales.loc[
    monthly_sales["orders"].idxmax()
]

highest_aov_month = monthly_sales.loc[
    monthly_sales["aov"].idxmax()
]


print("\n" + "=" * 70)
print("KEY BUSINESS INSIGHTS")
print("=" * 70)

print(
    f"Highest revenue month: "
    f"{highest_revenue_month['order_month']} "
    f"({highest_revenue_month['revenue']:,.2f})"
)

print(
    f"Highest order month: "
    f"{highest_order_month['order_month']} "
    f"({highest_order_month['orders']:,} orders)"
)

print(
    f"Highest AOV month: "
    f"{highest_aov_month['order_month']} "
    f"({highest_aov_month['aov']:,.2f})"
)


# ============================================================
# REVENUE TREND
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["order_month"],
    monthly_sales["revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# ORDER TREND
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["order_month"],
    monthly_sales["orders"],
    marker="o"
)

plt.title("Monthly Order Trend")
plt.xlabel("Month")
plt.ylabel("Number of Orders")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# SAVE MONTHLY ANALYSIS
# ============================================================

OUTPUT_FILE = (
    PROCESSED_DATA /
    "monthly_sales_analysis.csv"
)

monthly_sales.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved analysis to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("STEP 7.3 COMPLETED")
print("=" * 70)