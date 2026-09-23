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
# REFERENCE DATE
# ============================================================

reference_date = (
    sales["order_purchase_timestamp"].max()
    + pd.Timedelta(days=1)
)


print("\n" + "=" * 70)
print("RFM ANALYSIS")
print("=" * 70)

print(
    f"Reference date: "
    f"{reference_date.date()}"
)


# ============================================================
# BUILD RFM TABLE
# ============================================================

rfm = (
    sales
    .groupby("customer_unique_id")
    .agg(
        last_purchase=(
            "order_purchase_timestamp",
            "max"
        ),
        frequency=(
            "order_id",
            "nunique"
        ),
        monetary=(
            "revenue",
            "sum"
        )
    )
    .reset_index()
)


# ============================================================
# CALCULATE RECENCY
# ============================================================

rfm["recency"] = (
    reference_date
    - rfm["last_purchase"]
).dt.days


# ============================================================
# ROUND MONETARY
# ============================================================

rfm["monetary"] = rfm["monetary"].round(2)


# ============================================================
# RFM SCORES
# ============================================================

rfm["recency_score"] = pd.qcut(
    rfm["recency"],
    q=5,
    labels=[5, 4, 3, 2, 1],
    duplicates="drop"
).astype(int)


rfm["frequency_score"] = pd.qcut(
    rfm["frequency"].rank(
        method="first"
    ),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)


rfm["monetary_score"] = pd.qcut(
    rfm["monetary"].rank(
        method="first"
    ),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)


# ============================================================
# COMBINED RFM SCORE
# ============================================================

rfm["rfm_score"] = (
    rfm["recency_score"].astype(str)
    + rfm["frequency_score"].astype(str)
    + rfm["monetary_score"].astype(str)
)


# ============================================================
# RFM SEGMENTS
# ============================================================

def assign_segment(row):

    if (
        row["recency_score"] >= 4
        and row["frequency_score"] >= 4
        and row["monetary_score"] >= 4
    ):
        return "Champions"

    elif (
        row["recency_score"] >= 4
        and row["frequency_score"] >= 3
    ):
        return "Loyal Customers"

    elif (
        row["recency_score"] >= 4
        and row["monetary_score"] >= 4
    ):
        return "High Value New Customers"

    elif (
        row["recency_score"] <= 2
        and row["frequency_score"] >= 3
    ):
        return "At Risk"

    elif (
        row["recency_score"] <= 2
        and row["monetary_score"] >= 3
    ):
        return "High Value At Risk"

    elif (
        row["recency_score"] <= 2
    ):
        return "Inactive"

    else:
        return "Potential Loyalists"


rfm["customer_segment"] = rfm.apply(
    assign_segment,
    axis=1
)


# ============================================================
# DISPLAY RFM SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("RFM DATASET SUMMARY")
print("=" * 70)

print(
    f"Customers analyzed: "
    f"{len(rfm):,}"
)


# ============================================================
# SEGMENT DISTRIBUTION
# ============================================================

segment_summary = (
    rfm["customer_segment"]
    .value_counts()
    .reset_index()
)

segment_summary.columns = [
    "customer_segment",
    "customer_count"
]


segment_summary["percentage"] = (
    segment_summary["customer_count"]
    / len(rfm)
    * 100
).round(2)


print("\n" + "=" * 70)
print("CUSTOMER SEGMENT DISTRIBUTION")
print("=" * 70)

print(
    segment_summary.to_string(index=False)
)


# ============================================================
# SEGMENT VALUE ANALYSIS
# ============================================================

segment_value = (
    rfm
    .groupby("customer_segment")
    .agg(
        customers=("customer_unique_id", "count"),
        average_recency=("recency", "mean"),
        average_frequency=("frequency", "mean"),
        total_revenue=("monetary", "sum"),
        average_customer_value=("monetary", "mean")
    )
    .reset_index()
)


segment_value["average_recency"] = (
    segment_value["average_recency"]
    .round(2)
)

segment_value["average_frequency"] = (
    segment_value["average_frequency"]
    .round(2)
)

segment_value["total_revenue"] = (
    segment_value["total_revenue"]
    .round(2)
)

segment_value["average_customer_value"] = (
    segment_value["average_customer_value"]
    .round(2)
)


print("\n" + "=" * 70)
print("RFM SEGMENT VALUE ANALYSIS")
print("=" * 70)

print(
    segment_value
    .sort_values(
        "total_revenue",
        ascending=False
    )
    .to_string(index=False)
)


# ============================================================
# TOP CUSTOMERS
# ============================================================

top_customers = (
    rfm
    .sort_values(
        "monetary",
        ascending=False
    )
    .head(10)
)


print("\n" + "=" * 70)
print("TOP 10 CUSTOMERS BY MONETARY VALUE")
print("=" * 70)

print(
    top_customers[
        [
            "customer_unique_id",
            "recency",
            "frequency",
            "monetary",
            "rfm_score",
            "customer_segment"
        ]
    ].to_string(index=False)
)


# ============================================================
# SEGMENT DISTRIBUTION CHART
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    segment_summary["customer_segment"],
    segment_summary["customer_count"]
)

plt.title("Customer Segment Distribution")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()
plt.show()


# ============================================================
# SAVE RFM DATA
# ============================================================

RFM_OUTPUT = (
    PROCESSED_DATA /
    "rfm_customer_analysis.csv"
)

SEGMENT_OUTPUT = (
    PROCESSED_DATA /
    "rfm_segment_summary.csv"
)

VALUE_OUTPUT = (
    PROCESSED_DATA /
    "rfm_segment_value_analysis.csv"
)


rfm.to_csv(
    RFM_OUTPUT,
    index=False
)

segment_summary.to_csv(
    SEGMENT_OUTPUT,
    index=False
)

segment_value.to_csv(
    VALUE_OUTPUT,
    index=False
)


print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(RFM_OUTPUT)
print(SEGMENT_OUTPUT)
print(VALUE_OUTPUT)

print("\n" + "=" * 70)
print("STEP 7.8 COMPLETED")
print("=" * 70)