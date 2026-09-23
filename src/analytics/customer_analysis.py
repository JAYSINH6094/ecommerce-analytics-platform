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
# CUSTOMER ORDER SUMMARY
# ============================================================

customer_analysis = (
    sales
    .groupby("customer_unique_id")
    .agg(
        total_orders=("order_id", "nunique"),
        total_spent=("revenue", "sum"),
        first_purchase=("order_purchase_timestamp", "min"),
        last_purchase=("order_purchase_timestamp", "max")
    )
    .reset_index()
)


# ============================================================
# CUSTOMER TYPE
# ============================================================

customer_analysis["customer_type"] = customer_analysis[
    "total_orders"
].apply(
    lambda x: "Returning" if x > 1 else "One-Time"
)


# ============================================================
# ROUND REVENUE
# ============================================================

customer_analysis["total_spent"] = (
    customer_analysis["total_spent"].round(2)
)


# ============================================================
# CUSTOMER SUMMARY METRICS
# ============================================================

total_customers = len(customer_analysis)

one_time_customers = (
    customer_analysis["customer_type"]
    .eq("One-Time")
    .sum()
)

returning_customers = (
    customer_analysis["customer_type"]
    .eq("Returning")
    .sum()
)

repeat_customer_rate = (
    returning_customers / total_customers
) * 100

average_customer_value = (
    customer_analysis["total_spent"].mean()
)

average_orders_per_customer = (
    customer_analysis["total_orders"].mean()
)


# ============================================================
# DISPLAY CUSTOMER METRICS
# ============================================================

print("\n" + "=" * 70)
print("CUSTOMER ANALYTICS")
print("=" * 70)

print(
    f"Total unique customers: "
    f"{total_customers:,}"
)

print(
    f"One-time customers: "
    f"{one_time_customers:,}"
)

print(
    f"Returning customers: "
    f"{returning_customers:,}"
)

print(
    f"Repeat customer rate: "
    f"{repeat_customer_rate:.2f}%"
)

print(
    f"Average customer value: "
    f"{average_customer_value:.2f}"
)

print(
    f"Average orders per customer: "
    f"{average_orders_per_customer:.2f}"
)


# ============================================================
# CUSTOMER TYPE DISTRIBUTION
# ============================================================

customer_type_counts = (
    customer_analysis["customer_type"]
    .value_counts()
)


print("\n" + "=" * 70)
print("CUSTOMER TYPE DISTRIBUTION")
print("=" * 70)

print(customer_type_counts)


# ============================================================
# TOP 10 CUSTOMERS BY SPENDING
# ============================================================

top_customers = (
    customer_analysis
    .sort_values(
        "total_spent",
        ascending=False
    )
    .head(10)
)


print("\n" + "=" * 70)
print("TOP 10 CUSTOMERS BY SPENDING")
print("=" * 70)

print(
    top_customers[
        [
            "customer_unique_id",
            "total_orders",
            "total_spent",
            "customer_type"
        ]
    ].to_string(index=False)
)


# ============================================================
# CUSTOMER TYPE CHART
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    customer_type_counts.index,
    customer_type_counts.values
)

plt.title("One-Time vs Returning Customers")
plt.xlabel("Customer Type")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()


# ============================================================
# TOP CUSTOMERS CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.barh(
    top_customers["customer_unique_id"][::-1],
    top_customers["total_spent"][::-1]
)

plt.title("Top 10 Customers by Total Spending")
plt.xlabel("Total Spending")
plt.ylabel("Customer ID")

plt.tight_layout()
plt.show()


# ============================================================
# SAVE CUSTOMER ANALYSIS
# ============================================================

OUTPUT_FILE = (
    PROCESSED_DATA /
    "customer_analysis.csv"
)

customer_analysis.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved customer analysis to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("STEP 7.5 COMPLETED")
print("=" * 70)