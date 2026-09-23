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
# CONVERT DATE
# ============================================================

sales["order_purchase_timestamp"] = pd.to_datetime(
    sales["order_purchase_timestamp"]
)


# ============================================================
# CREATE PURCHASE MONTH
# ============================================================

sales["purchase_month"] = (
    sales["order_purchase_timestamp"]
    .dt.to_period("M")
)


# ============================================================
# FIND CUSTOMER'S FIRST PURCHASE
# ============================================================

customer_first_purchase = (
    sales
    .groupby("customer_unique_id")["purchase_month"]
    .min()
    .reset_index()
)

customer_first_purchase.columns = [
    "customer_unique_id",
    "cohort_month"
]


# ============================================================
# ADD COHORT MONTH TO SALES
# ============================================================

sales = sales.merge(
    customer_first_purchase,
    on="customer_unique_id",
    how="left"
)


# ============================================================
# CALCULATE MONTHS SINCE FIRST PURCHASE
# ============================================================

sales["cohort_year"] = (
    sales["cohort_month"].dt.year
)

sales["cohort_month_number"] = (
    sales["cohort_month"].dt.month
)

sales["purchase_year"] = (
    sales["purchase_month"].dt.year
)

sales["purchase_month_number"] = (
    sales["purchase_month"].dt.month
)


sales["months_since_first_purchase"] = (
    (
        sales["purchase_year"]
        - sales["cohort_year"]
    ) * 12
    +
    (
        sales["purchase_month_number"]
        - sales["cohort_month_number"]
    )
)


# ============================================================
# COHORT CUSTOMER COUNTS
# ============================================================

cohort_data = (
    sales[
        [
            "customer_unique_id",
            "cohort_month",
            "purchase_month",
            "months_since_first_purchase"
        ]
    ]
    .drop_duplicates()
)


cohort_counts = (
    cohort_data
    .groupby(
        [
            "cohort_month",
            "months_since_first_purchase"
        ]
    )["customer_unique_id"]
    .nunique()
    .reset_index()
)


cohort_counts.columns = [
    "cohort_month",
    "months_since_first_purchase",
    "active_customers"
]


# ============================================================
# COHORT SIZE
# ============================================================

cohort_sizes = (
    cohort_counts[
        cohort_counts["months_since_first_purchase"] == 0
    ][
        [
            "cohort_month",
            "active_customers"
        ]
    ]
    .rename(
        columns={
            "active_customers": "cohort_size"
        }
    )
)


# ============================================================
# CALCULATE RETENTION
# ============================================================

cohort_counts = cohort_counts.merge(
    cohort_sizes,
    on="cohort_month",
    how="left"
)


cohort_counts["retention_percentage"] = (
    cohort_counts["active_customers"]
    / cohort_counts["cohort_size"]
    * 100
)


cohort_counts["retention_percentage"] = (
    cohort_counts["retention_percentage"]
    .round(2)
)


# ============================================================
# RETENTION MATRIX
# ============================================================

retention_matrix = (
    cohort_counts
    .pivot(
        index="cohort_month",
        columns="months_since_first_purchase",
        values="retention_percentage"
    )
)


# ============================================================
# DISPLAY COHORT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("COHORT ANALYSIS")
print("=" * 70)

print(
    f"Total cohorts: "
    f"{retention_matrix.shape[0]}"
)


print("\n" + "=" * 70)
print("RETENTION MATRIX")
print("=" * 70)

print(
    retention_matrix.to_string()
)


# ============================================================
# FIRST-MONTH RETENTION
# ============================================================

first_month_retention = (
    cohort_counts[
        cohort_counts["months_since_first_purchase"] == 1
    ]
)


print("\n" + "=" * 70)
print("FIRST-MONTH RETENTION")
print("=" * 70)

if len(first_month_retention) > 0:

    print(
        f"Average first-month retention: "
        f"{first_month_retention['retention_percentage'].mean():.2f}%"
    )

    print(
        f"Highest first-month retention: "
        f"{first_month_retention['retention_percentage'].max():.2f}%"
    )

    print(
        f"Lowest first-month retention: "
        f"{first_month_retention['retention_percentage'].min():.2f}%"
    )

else:

    print(
        "No cohort has enough follow-up data "
        "to calculate first-month retention."
    )


# ============================================================
# RETENTION HEATMAP
# ============================================================

plt.figure(figsize=(14, 10))

plt.imshow(
    retention_matrix,
    aspect="auto",
    interpolation="nearest"
)

plt.colorbar(
    label="Retention %"
)

plt.title("Customer Cohort Retention")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort Month")

plt.xticks(
    range(len(retention_matrix.columns)),
    retention_matrix.columns
)

plt.yticks(
    range(len(retention_matrix.index)),
    retention_matrix.index.astype(str)
)

plt.tight_layout()
plt.show()


# ============================================================
# SAVE COHORT RESULTS
# ============================================================

COHORT_OUTPUT = (
    PROCESSED_DATA /
    "cohort_analysis.csv"
)

RETENTION_OUTPUT = (
    PROCESSED_DATA /
    "cohort_retention_matrix.csv"
)


cohort_counts.to_csv(
    COHORT_OUTPUT,
    index=False
)

retention_matrix.to_csv(
    RETENTION_OUTPUT
)


print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(COHORT_OUTPUT)
print(RETENTION_OUTPUT)

print("\n" + "=" * 70)
print("STEP 7.9 COMPLETED")
print("=" * 70)