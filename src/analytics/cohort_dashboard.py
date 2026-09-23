import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


# ============================================================
# LOAD REAL SALES DATA
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
# PREPARE ORDER-LEVEL DATA
# ============================================================

orders = (
    sales[
        [
            "order_id",
            "customer_unique_id",
            "order_purchase_timestamp",
            "revenue"
        ]
    ]
    .groupby(
        [
            "order_id",
            "customer_unique_id",
            "order_purchase_timestamp"
        ],
        as_index=False
    )
    .agg(
        revenue=("revenue", "sum")
    )
)


# ============================================================
# COHORT ASSIGNMENT
# ============================================================

orders["order_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
    .dt.to_timestamp()
)


customer_first_purchase = (
    orders
    .groupby("customer_unique_id")
    ["order_purchase_timestamp"]
    .min()
    .reset_index()
)

customer_first_purchase.columns = [
    "customer_unique_id",
    "first_purchase_timestamp"
]

customer_first_purchase["cohort_month"] = (
    customer_first_purchase["first_purchase_timestamp"]
    .dt.to_period("M")
    .dt.to_timestamp()
)


orders = orders.merge(
    customer_first_purchase[
        [
            "customer_unique_id",
            "cohort_month"
        ]
    ],
    on="customer_unique_id",
    how="left"
)


# ============================================================
# MONTHS SINCE ACQUISITION
# ============================================================

orders["months_since_acquisition"] = (
    (
        orders["order_month"].dt.year
        - orders["cohort_month"].dt.year
    ) * 12
    +
    (
        orders["order_month"].dt.month
        - orders["cohort_month"].dt.month
    )
)


# ============================================================
# COHORT CUSTOMER COUNTS
# ============================================================

cohort_size = (
    orders
    .groupby("cohort_month")
    ["customer_unique_id"]
    .nunique()
    .reset_index(name="cohort_customers")
)


# ============================================================
# ACTIVE CUSTOMERS BY COHORT MONTH
# ============================================================

cohort_activity = (
    orders
    .groupby(
        [
            "cohort_month",
            "months_since_acquisition"
        ]
    )
    .agg(
        active_customers=(
            "customer_unique_id",
            "nunique"
        ),
        orders=(
            "order_id",
            "nunique"
        ),
        revenue=(
            "revenue",
            "sum"
        )
    )
    .reset_index()
)


# ============================================================
# ADD COHORT SIZE
# ============================================================

cohort_activity = cohort_activity.merge(
    cohort_size,
    on="cohort_month",
    how="left"
)


# ============================================================
# RETENTION RATE
# ============================================================

cohort_activity["retention_rate"] = (
    cohort_activity["active_customers"]
    / cohort_activity["cohort_customers"]
    * 100
)


# ============================================================
# REVENUE PER ACTIVE CUSTOMER
# ============================================================

cohort_activity["revenue_per_active_customer"] = (
    cohort_activity["revenue"]
    / cohort_activity["active_customers"]
)


cohort_activity[
    [
        "retention_rate",
        "revenue_per_active_customer"
    ]
] = cohort_activity[
    [
        "retention_rate",
        "revenue_per_active_customer"
    ]
].round(2)


# ============================================================
# RETENTION MATRIX
# ============================================================

retention_matrix = (
    cohort_activity
    .pivot(
        index="cohort_month",
        columns="months_since_acquisition",
        values="retention_rate"
    )
)


# ============================================================
# COHORT REVENUE MATRIX
# ============================================================

revenue_matrix = (
    cohort_activity
    .pivot(
        index="cohort_month",
        columns="months_since_acquisition",
        values="revenue"
    )
)


# ============================================================
# FIRST-MONTH RETENTION
# ============================================================

first_month_retention = cohort_activity[
    cohort_activity["months_since_acquisition"] == 1
].copy()


# ============================================================
# SUMMARY METRICS
# ============================================================

total_cohorts = (
    cohort_activity["cohort_month"]
    .nunique()
)

average_first_month_retention = (
    first_month_retention["retention_rate"]
    .mean()
)

highest_first_month_retention = (
    first_month_retention["retention_rate"]
    .max()
)

lowest_first_month_retention = (
    first_month_retention["retention_rate"]
    .min()
)


print("\n" + "=" * 70)
print("COHORT & RETENTION DASHBOARD ANALYSIS")
print("=" * 70)

print(
    f"Cohorts analyzed: {total_cohorts}"
)

print(
    f"Average first-month retention: "
    f"{average_first_month_retention:.2f}%"
)

print(
    f"Highest first-month retention: "
    f"{highest_first_month_retention:.2f}%"
)

print(
    f"Lowest first-month retention: "
    f"{lowest_first_month_retention:.2f}%"
)


# ============================================================
# COHORT SUMMARY
# ============================================================

cohort_summary = (
    cohort_activity
    .groupby("cohort_month")
    .agg(
        cohort_customers=("cohort_customers", "first"),
        total_orders=("orders", "sum"),
        total_revenue=("revenue", "sum"),
        first_month_retention=(
            "retention_rate",
            lambda x: (
                x.iloc[1]
                if len(x) > 1
                else None
            )
        ),
        average_retention=("retention_rate", "mean")
    )
    .reset_index()
)


cohort_summary[
    [
        "total_revenue",
        "first_month_retention",
        "average_retention"
    ]
] = cohort_summary[
    [
        "total_revenue",
        "first_month_retention",
        "average_retention"
    ]
].round(2)


print("\n" + "=" * 70)
print("COHORT SUMMARY")
print("=" * 70)

print(
    cohort_summary.to_string(index=False)
)


# ============================================================
# RETENTION MATRIX OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("RETENTION MATRIX")
print("=" * 70)

print(
    retention_matrix.round(2).to_string()
)


# ============================================================
# SAVE DASHBOARD DATA
# ============================================================

cohort_activity.to_csv(
    PROCESSED_DATA / "cohort_dashboard.csv",
    index=False
)


cohort_summary.to_csv(
    PROCESSED_DATA / "cohort_dashboard_summary.csv",
    index=False
)


retention_matrix.to_csv(
    PROCESSED_DATA / "cohort_retention_dashboard.csv"
)


revenue_matrix.to_csv(
    PROCESSED_DATA / "cohort_revenue_matrix.csv"
)


print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(
    PROCESSED_DATA / "cohort_dashboard.csv"
)

print(
    PROCESSED_DATA / "cohort_dashboard_summary.csv"
)

print(
    PROCESSED_DATA / "cohort_retention_dashboard.csv"
)

print(
    PROCESSED_DATA / "cohort_revenue_matrix.csv"
)


print("\n" + "=" * 70)
print("STEP 9 COMPLETED")
print("=" * 70)