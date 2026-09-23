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
# CUSTOMER-LEVEL RFM
# ============================================================

reference_date = (
    sales["order_purchase_timestamp"].max()
    + pd.Timedelta(days=1)
)

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
# RECENCY
# ============================================================

rfm["recency"] = (
    reference_date
    - rfm["last_purchase"]
).dt.days


# ============================================================
# RFM QUINTILE SCORES
# ============================================================

# Recency:
# Lower number of days = better customer activity.
# Therefore the scoring direction is reversed.

rfm["R_score"] = pd.qcut(
    rfm["recency"],
    q=5,
    labels=[5, 4, 3, 2, 1],
    duplicates="drop"
).astype(int)


# Frequency:
# Higher frequency = better.

rfm["F_score"] = pd.qcut(
    rfm["frequency"].rank(
        method="first"
    ),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)


# Monetary:
# Higher spending = better.

rfm["M_score"] = pd.qcut(
    rfm["monetary"].rank(
        method="first"
    ),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)


# ============================================================
# COMBINED RFM SCORE
# ============================================================

rfm["RFM_score"] = (
    rfm["R_score"].astype(str)
    + rfm["F_score"].astype(str)
    + rfm["M_score"].astype(str)
)


rfm["RFM_total_score"] = (
    rfm["R_score"]
    + rfm["F_score"]
    + rfm["M_score"]
)


# ============================================================
# CUSTOMER SEGMENTS
# ============================================================

def assign_segment(row):

    r = row["R_score"]
    f = row["F_score"]
    m = row["M_score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 4 and f >= 3 and m >= 3:
        return "Loyal Customers"

    elif r >= 4 and f <= 2 and m >= 4:
        return "High Value New Customers"

    elif r <= 2 and m >= 4:
        return "High Value At Risk"

    elif r <= 2 and f >= 2:
        return "At Risk"

    elif r >= 3 and f <= 2:
        return "Potential Loyalists"

    else:
        return "Inactive"


rfm["segment"] = rfm.apply(
    assign_segment,
    axis=1
)


# ============================================================
# CUSTOMER VALUE
# ============================================================

rfm["average_order_value"] = (
    rfm["monetary"]
    / rfm["frequency"]
).round(2)


# ============================================================
# SEGMENT SUMMARY
# ============================================================

segment_summary = (
    rfm
    .groupby("segment")
    .agg(
        customers=("customer_unique_id", "count"),
        total_revenue=("monetary", "sum"),
        average_revenue=("monetary", "mean"),
        average_recency=("recency", "mean"),
        average_frequency=("frequency", "mean"),
        average_order_value=("average_order_value", "mean")
    )
    .reset_index()
)


total_customers = len(rfm)
total_revenue = rfm["monetary"].sum()


segment_summary["customer_percentage"] = (
    segment_summary["customers"]
    / total_customers
    * 100
)

segment_summary["revenue_percentage"] = (
    segment_summary["total_revenue"]
    / total_revenue
    * 100
)


segment_numeric_columns = [
    "total_revenue",
    "average_revenue",
    "average_recency",
    "average_frequency",
    "average_order_value",
    "customer_percentage",
    "revenue_percentage"
]


segment_summary[segment_numeric_columns] = (
    segment_summary[segment_numeric_columns]
    .round(2)
)


# ============================================================
# SORT SEGMENTS BY REVENUE
# ============================================================

segment_summary = segment_summary.sort_values(
    "total_revenue",
    ascending=False
)


# ============================================================
# RFM SCORE DISTRIBUTION
# ============================================================

rfm_score_summary = (
    rfm
    .groupby("RFM_total_score")
    .agg(
        customers=("customer_unique_id", "count"),
        total_revenue=("monetary", "sum"),
        average_recency=("recency", "mean"),
        average_frequency=("frequency", "mean"),
        average_monetary=("monetary", "mean")
    )
    .reset_index()
    .sort_values("RFM_total_score", ascending=False)
)


rfm_score_summary[
    [
        "total_revenue",
        "average_recency",
        "average_frequency",
        "average_monetary"
    ]
] = rfm_score_summary[
    [
        "total_revenue",
        "average_recency",
        "average_frequency",
        "average_monetary"
    ]
].round(2)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("RFM DASHBOARD ANALYSIS")
print("=" * 70)

print(
    f"Reference date: "
    f"{reference_date.strftime('%Y-%m-%d')}"
)

print(
    f"Customers analyzed: "
    f"{total_customers:,}"
)

print(
    f"Total customer revenue: "
    f"{total_revenue:,.2f}"
)


print("\n" + "=" * 70)
print("RFM SEGMENT SUMMARY")
print("=" * 70)

print(
    segment_summary.to_string(index=False)
)


print("\n" + "=" * 70)
print("RFM SCORE DISTRIBUTION")
print("=" * 70)

print(
    rfm_score_summary.to_string(index=False)
)


# ============================================================
# TOP CUSTOMERS
# ============================================================

top_rfm_customers = (
    rfm
    .sort_values(
        ["RFM_total_score", "monetary"],
        ascending=[False, False]
    )
    .head(20)
)


print("\n" + "=" * 70)
print("TOP 20 RFM CUSTOMERS")
print("=" * 70)

print(
    top_rfm_customers[
        [
            "customer_unique_id",
            "recency",
            "frequency",
            "monetary",
            "RFM_score",
            "RFM_total_score",
            "segment"
        ]
    ].to_string(index=False)
)


# ============================================================
# SAVE DASHBOARD-READY DATA
# ============================================================

rfm_dashboard = rfm[
    [
        "customer_unique_id",
        "last_purchase",
        "recency",
        "frequency",
        "monetary",
        "average_order_value",
        "R_score",
        "F_score",
        "M_score",
        "RFM_score",
        "RFM_total_score",
        "segment"
    ]
].copy()


rfm_dashboard.to_csv(
    PROCESSED_DATA / "rfm_dashboard.csv",
    index=False
)


segment_summary.to_csv(
    PROCESSED_DATA / "rfm_dashboard_segments.csv",
    index=False
)


rfm_score_summary.to_csv(
    PROCESSED_DATA / "rfm_score_summary.csv",
    index=False
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(
    PROCESSED_DATA / "rfm_dashboard.csv"
)

print(
    PROCESSED_DATA / "rfm_dashboard_segments.csv"
)

print(
    PROCESSED_DATA / "rfm_score_summary.csv"
)

print("\n" + "=" * 70)
print("STEP 8 COMPLETED")
print("=" * 70)