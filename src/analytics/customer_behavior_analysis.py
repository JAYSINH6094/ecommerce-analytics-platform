import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


# ============================================================
# LOAD ANALYSIS DATA
# ============================================================

sales = pd.read_csv(
    PROCESSED_DATA / "analysis_ready_sales.csv"
)

sales["order_purchase_timestamp"] = pd.to_datetime(
    sales["order_purchase_timestamp"],
    errors="coerce"
)

sales["revenue"] = pd.to_numeric(
    sales["revenue"],
    errors="coerce"
)


# ============================================================
# CUSTOMER-LEVEL ORDER DATA
# ============================================================

customer_orders = (
    sales
    .groupby("customer_unique_id")
    .agg(
        order_count=("order_id", "nunique"),
        revenue=("revenue", "sum"),
        average_order_value=("revenue", "mean"),
        first_purchase=("order_purchase_timestamp", "min"),
        last_purchase=("order_purchase_timestamp", "max")
    )
    .reset_index()
)


# ============================================================
# CUSTOMER TYPE
# ============================================================

customer_orders["customer_type"] = customer_orders[
    "order_count"
].apply(
    lambda x: "Returning Customer"
    if x > 1
    else "One-Time Customer"
)


# ============================================================
# PURCHASE FREQUENCY GROUP
# ============================================================

def frequency_group(order_count):
    if order_count == 1:
        return "1 Order"
    elif order_count == 2:
        return "2 Orders"
    elif order_count <= 4:
        return "3-4 Orders"
    else:
        return "5+ Orders"


customer_orders["purchase_frequency_group"] = (
    customer_orders["order_count"]
    .apply(frequency_group)
)


# ============================================================
# CUSTOMER LIFESPAN
# ============================================================

customer_orders["customer_lifespan_days"] = (
    customer_orders["last_purchase"]
    - customer_orders["first_purchase"]
).dt.total_seconds() / (60 * 60 * 24)

customer_orders["customer_lifespan_days"] = (
    customer_orders["customer_lifespan_days"]
    .round(2)
)


# ============================================================
# OVERALL CUSTOMER BEHAVIOR
# ============================================================

total_customers = len(customer_orders)

one_time_customers = (
    customer_orders["customer_type"]
    == "One-Time Customer"
).sum()

returning_customers = (
    customer_orders["customer_type"]
    == "Returning Customer"
).sum()

total_customer_revenue = customer_orders["revenue"].sum()

average_customer_revenue = (
    customer_orders["revenue"].mean()
)

average_orders_per_customer = (
    customer_orders["order_count"].mean()
)

repeat_customer_rate = (
    returning_customers
    / total_customers
    * 100
)


print("\n" + "=" * 70)
print("CUSTOMER BEHAVIOR ANALYSIS")
print("=" * 70)

print(f"Total customers: {total_customers:,}")
print(f"One-time customers: {one_time_customers:,}")
print(f"Returning customers: {returning_customers:,}")
print(f"Repeat customer rate: {repeat_customer_rate:.2f}%")
print(
    f"Average orders per customer: "
    f"{average_orders_per_customer:.2f}"
)
print(
    f"Average customer revenue: "
    f"{average_customer_revenue:,.2f}"
)


# ============================================================
# CUSTOMER TYPE ANALYSIS
# ============================================================

customer_type_analysis = (
    customer_orders
    .groupby("customer_type")
    .agg(
        customers=("customer_unique_id", "count"),
        total_orders=("order_count", "sum"),
        total_revenue=("revenue", "sum"),
        average_revenue=("revenue", "mean"),
        average_orders=("order_count", "mean"),
        average_order_value=("average_order_value", "mean")
    )
    .reset_index()
)

customer_type_analysis["customer_percentage"] = (
    customer_type_analysis["customers"]
    / total_customers
    * 100
)

customer_type_analysis["revenue_percentage"] = (
    customer_type_analysis["total_revenue"]
    / total_customer_revenue
    * 100
)

numeric_columns = [
    "total_revenue",
    "average_revenue",
    "average_orders",
    "average_order_value",
    "customer_percentage",
    "revenue_percentage"
]

customer_type_analysis[numeric_columns] = (
    customer_type_analysis[numeric_columns]
    .round(2)
)

print("\n" + "=" * 70)
print("CUSTOMER TYPE PERFORMANCE")
print("=" * 70)

print(
    customer_type_analysis
    .to_string(index=False)
)


# ============================================================
# PURCHASE FREQUENCY ANALYSIS
# ============================================================

frequency_analysis = (
    customer_orders
    .groupby("purchase_frequency_group")
    .agg(
        customers=("customer_unique_id", "count"),
        total_orders=("order_count", "sum"),
        total_revenue=("revenue", "sum"),
        average_customer_revenue=("revenue", "mean"),
        average_order_value=("average_order_value", "mean")
    )
    .reset_index()
)

frequency_analysis["customer_percentage"] = (
    frequency_analysis["customers"]
    / total_customers
    * 100
)

frequency_analysis["revenue_percentage"] = (
    frequency_analysis["total_revenue"]
    / total_customer_revenue
    * 100
)

frequency_numeric_columns = [
    "total_revenue",
    "average_customer_revenue",
    "average_order_value",
    "customer_percentage",
    "revenue_percentage"
]

frequency_analysis[frequency_numeric_columns] = (
    frequency_analysis[frequency_numeric_columns]
    .round(2)
)

# Keep logical frequency order
frequency_order = [
    "1 Order",
    "2 Orders",
    "3-4 Orders",
    "5+ Orders"
]

frequency_analysis["purchase_frequency_group"] = pd.Categorical(
    frequency_analysis["purchase_frequency_group"],
    categories=frequency_order,
    ordered=True
)

frequency_analysis = frequency_analysis.sort_values(
    "purchase_frequency_group"
)


print("\n" + "=" * 70)
print("PURCHASE FREQUENCY ANALYSIS")
print("=" * 70)

print(
    frequency_analysis
    .to_string(index=False)
)


# ============================================================
# TOP CUSTOMERS BY REVENUE
# ============================================================

top_customers = (
    customer_orders
    .sort_values("revenue", ascending=False)
    .head(20)
    .copy()
)

top_customers["revenue"] = (
    top_customers["revenue"].round(2)
)

top_customers["average_order_value"] = (
    top_customers["average_order_value"].round(2)
)


print("\n" + "=" * 70)
print("TOP 20 CUSTOMERS BY REVENUE")
print("=" * 70)

print(
    top_customers[
        [
            "customer_unique_id",
            "order_count",
            "revenue",
            "average_order_value",
            "customer_type"
        ]
    ].to_string(index=False)
)


# ============================================================
# REVENUE CONCENTRATION
# ============================================================

customer_ranked = customer_orders.sort_values(
    "revenue",
    ascending=False
).copy()

customer_ranked["cumulative_revenue"] = (
    customer_ranked["revenue"].cumsum()
)

customer_ranked["cumulative_revenue_percentage"] = (
    customer_ranked["cumulative_revenue"]
    / total_customer_revenue
    * 100
)

top_10_percent_count = max(
    1,
    int(total_customers * 0.10)
)

top_10_percent_revenue = (
    customer_ranked
    .head(top_10_percent_count)["revenue"]
    .sum()
)

top_10_percent_revenue_percentage = (
    top_10_percent_revenue
    / total_customer_revenue
    * 100
)

print("\n" + "=" * 70)
print("REVENUE CONCENTRATION")
print("=" * 70)

print(
    f"Top 10% customers revenue: "
    f"{top_10_percent_revenue:,.2f}"
)

print(
    f"Top 10% revenue contribution: "
    f"{top_10_percent_revenue_percentage:.2f}%"
)


# ============================================================
# CHART 1: CUSTOMER TYPE DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    customer_type_analysis["customer_type"],
    customer_type_analysis["customers"]
)

plt.title("One-Time vs Returning Customers")
plt.xlabel("Customer Type")
plt.ylabel("Number of Customers")

plt.xticks(rotation=15)
plt.tight_layout()

plt.show()


# ============================================================
# CHART 2: REVENUE BY PURCHASE FREQUENCY
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    frequency_analysis["purchase_frequency_group"].astype(str),
    frequency_analysis["total_revenue"]
)

plt.title("Revenue by Customer Purchase Frequency")
plt.xlabel("Purchase Frequency")
plt.ylabel("Total Revenue")

plt.tight_layout()

plt.show()


# ============================================================
# SAVE RESULTS
# ============================================================

customer_behavior_analysis = customer_orders.copy()

customer_behavior_analysis.to_csv(
    PROCESSED_DATA / "customer_behavior_analysis.csv",
    index=False
)

customer_type_analysis.to_csv(
    PROCESSED_DATA / "customer_type_analysis.csv",
    index=False
)

frequency_analysis.to_csv(
    PROCESSED_DATA / "customer_frequency_analysis.csv",
    index=False
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(
    PROCESSED_DATA
    / "customer_behavior_analysis.csv"
)

print(
    PROCESSED_DATA
    / "customer_type_analysis.csv"
)

print(
    PROCESSED_DATA
    / "customer_frequency_analysis.csv"
)

print("\n" + "=" * 70)
print("STEP 7.13 COMPLETED")
print("=" * 70)