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

orders = pd.read_csv(
    PROCESSED_DATA / "orders.csv"
)

sales = pd.read_csv(
    PROCESSED_DATA / "analysis_ready_sales.csv"
)


# ============================================================
# CONVERT DATE COLUMNS
# ============================================================

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )


# ============================================================
# KEEP DELIVERED ORDERS WITH DELIVERY DATES
# ============================================================

delivery = orders[
    (orders["order_status"] == "delivered")
    &
    (orders["order_delivered_customer_date"].notna())
    &
    (orders["order_estimated_delivery_date"].notna())
].copy()


# ============================================================
# DELIVERY TIME
# ============================================================

delivery["delivery_days"] = (
    delivery["order_delivered_customer_date"]
    - delivery["order_purchase_timestamp"]
).dt.total_seconds() / (60 * 60 * 24)


# ============================================================
# DELIVERY DELAY
# ============================================================

delivery["delivery_delay_days"] = (
    delivery["order_delivered_customer_date"]
    - delivery["order_estimated_delivery_date"]
).dt.total_seconds() / (60 * 60 * 24)


# ============================================================
# ON-TIME / LATE CLASSIFICATION
# ============================================================

delivery["delivery_status"] = delivery[
    "delivery_delay_days"
].apply(
    lambda x: "Late" if x > 0 else "On Time"
)


# ============================================================
# ROUND VALUES
# ============================================================

delivery["delivery_days"] = (
    delivery["delivery_days"].round(2)
)

delivery["delivery_delay_days"] = (
    delivery["delivery_delay_days"].round(2)
)


# ============================================================
# OVERALL DELIVERY METRICS
# ============================================================

average_delivery_days = (
    delivery["delivery_days"].mean()
)

median_delivery_days = (
    delivery["delivery_days"].median()
)

average_delay_days = (
    delivery["delivery_delay_days"].mean()
)

late_orders = (
    delivery["delivery_status"] == "Late"
).sum()

on_time_orders = (
    delivery["delivery_status"] == "On Time"
).sum()

total_delivery_orders = len(delivery)

late_percentage = (
    late_orders
    / total_delivery_orders
    * 100
)

on_time_percentage = (
    on_time_orders
    / total_delivery_orders
    * 100
)


# ============================================================
# DISPLAY OVERALL METRICS
# ============================================================

print("\n" + "=" * 70)
print("DELIVERY PERFORMANCE ANALYSIS")
print("=" * 70)

print(
    f"Delivered orders analyzed: "
    f"{total_delivery_orders:,}"
)

print(
    f"Average delivery time: "
    f"{average_delivery_days:.2f} days"
)

print(
    f"Median delivery time: "
    f"{median_delivery_days:.2f} days"
)

print(
    f"Average delivery delay: "
    f"{average_delay_days:.2f} days"
)

print(
    f"On-time orders: "
    f"{on_time_orders:,} "
    f"({on_time_percentage:.2f}%)"
)

print(
    f"Late orders: "
    f"{late_orders:,} "
    f"({late_percentage:.2f}%)"
)


# ============================================================
# DELIVERY STATUS DISTRIBUTION
# ============================================================

delivery_status_summary = (
    delivery["delivery_status"]
    .value_counts()
    .reset_index()
)

delivery_status_summary.columns = [
    "delivery_status",
    "order_count"
]

delivery_status_summary["percentage"] = (
    delivery_status_summary["order_count"]
    / total_delivery_orders
    * 100
).round(2)


print("\n" + "=" * 70)
print("DELIVERY STATUS")
print("=" * 70)

print(
    delivery_status_summary.to_string(index=False)
)


# ============================================================
# DELIVERY PERFORMANCE BY STATE
# ============================================================

delivery_state = delivery[
    [
        "order_id",
        "customer_id",
        "delivery_days",
        "delivery_delay_days",
        "delivery_status"
    ]
].merge(
    sales[
        [
            "order_id",
            "customer_state"
        ]
    ].drop_duplicates("order_id"),
    on="order_id",
    how="inner"
)


state_delivery = (
    delivery_state
    .groupby("customer_state")
    .agg(
        orders=("order_id", "count"),
        average_delivery_days=("delivery_days", "mean"),
        average_delay_days=("delivery_delay_days", "mean"),
        late_orders=(
            "delivery_status",
            lambda x: (x == "Late").sum()
        )
    )
    .reset_index()
)


state_delivery["late_percentage"] = (
    state_delivery["late_orders"]
    / state_delivery["orders"]
    * 100
)


state_delivery["average_delivery_days"] = (
    state_delivery["average_delivery_days"]
    .round(2)
)

state_delivery["average_delay_days"] = (
    state_delivery["average_delay_days"]
    .round(2)
)

state_delivery["late_percentage"] = (
    state_delivery["late_percentage"]
    .round(2)
)


state_delivery = state_delivery.sort_values(
    "orders",
    ascending=False
)


print("\n" + "=" * 70)
print("DELIVERY PERFORMANCE BY STATE")
print("=" * 70)

print(
    state_delivery
    .head(10)
    .to_string(index=False)
)


# ============================================================
# DELIVERY PERFORMANCE BY CATEGORY
# ============================================================

delivery_category = delivery[
    [
        "order_id",
        "delivery_days",
        "delivery_delay_days",
        "delivery_status"
    ]
].merge(
    sales[
        [
            "order_id",
            "product_category_name_english"
        ]
    ].drop_duplicates("order_id"),
    on="order_id",
    how="inner"
)


category_delivery = (
    delivery_category
    .groupby("product_category_name_english")
    .agg(
        orders=("order_id", "count"),
        average_delivery_days=("delivery_days", "mean"),
        average_delay_days=("delivery_delay_days", "mean"),
        late_orders=(
            "delivery_status",
            lambda x: (x == "Late").sum()
        )
    )
    .reset_index()
)


category_delivery["late_percentage"] = (
    category_delivery["late_orders"]
    / category_delivery["orders"]
    * 100
)


category_delivery["average_delivery_days"] = (
    category_delivery["average_delivery_days"]
    .round(2)
)

category_delivery["average_delay_days"] = (
    category_delivery["average_delay_days"]
    .round(2)
)

category_delivery["late_percentage"] = (
    category_delivery["late_percentage"]
    .round(2)
)


category_delivery = category_delivery.sort_values(
    "orders",
    ascending=False
)


print("\n" + "=" * 70)
print("DELIVERY PERFORMANCE BY CATEGORY")
print("=" * 70)

print(
    category_delivery
    .head(10)
    .to_string(index=False)
)


# ============================================================
# DELIVERY STATUS CHART
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    delivery_status_summary["delivery_status"],
    delivery_status_summary["order_count"]
)

plt.title("On-Time vs Late Deliveries")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()


# ============================================================
# DELIVERY TIME DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    delivery["delivery_days"],
    bins=50
)

plt.title("Delivery Time Distribution")
plt.xlabel("Delivery Time (Days)")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()


# ============================================================
# SAVE RESULTS
# ============================================================

DELIVERY_OUTPUT = (
    PROCESSED_DATA /
    "delivery_analysis.csv"
)

STATE_OUTPUT = (
    PROCESSED_DATA /
    "state_delivery_analysis.csv"
)

CATEGORY_OUTPUT = (
    PROCESSED_DATA /
    "category_delivery_analysis.csv"
)


delivery.to_csv(
    DELIVERY_OUTPUT,
    index=False
)

state_delivery.to_csv(
    STATE_OUTPUT,
    index=False
)

category_delivery.to_csv(
    CATEGORY_OUTPUT,
    index=False
)


print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(DELIVERY_OUTPUT)
print(STATE_OUTPUT)
print(CATEGORY_OUTPUT)

print("\n" + "=" * 70)
print("STEP 7.11 COMPLETED")
print("=" * 70)