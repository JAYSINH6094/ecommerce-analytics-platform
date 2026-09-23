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

payments = pd.read_csv(PROCESSED_DATA / "payments.csv")
orders = pd.read_csv(PROCESSED_DATA / "orders.csv")


# ============================================================
# FILTER DELIVERED ORDERS
# ============================================================

delivered_orders = orders[
    orders["order_status"] == "delivered"
][["order_id"]].copy()

payment_data = payments.merge(
    delivered_orders,
    on="order_id",
    how="inner"
)


# ============================================================
# BASIC PAYMENT CLEANING
# ============================================================

payment_data["payment_value"] = pd.to_numeric(
    payment_data["payment_value"],
    errors="coerce"
)

payment_data["payment_installments"] = pd.to_numeric(
    payment_data["payment_installments"],
    errors="coerce"
)

payment_data["payment_sequential"] = pd.to_numeric(
    payment_data["payment_sequential"],
    errors="coerce"
)


# ============================================================
# OVERALL PAYMENT METRICS
# ============================================================

total_payment_records = len(payment_data)

total_payment_value = payment_data["payment_value"].sum()

average_payment_value = payment_data["payment_value"].mean()

median_payment_value = payment_data["payment_value"].median()

unique_paid_orders = payment_data["order_id"].nunique()

average_installments = payment_data["payment_installments"].mean()

print("\n" + "=" * 70)
print("PAYMENT & REVENUE ANALYSIS")
print("=" * 70)

print(f"Payment records analyzed: {total_payment_records:,}")
print(f"Orders with payment records: {unique_paid_orders:,}")
print(f"Total payment value: {total_payment_value:,.2f}")
print(f"Average payment value: {average_payment_value:,.2f}")
print(f"Median payment value: {median_payment_value:,.2f}")
print(f"Average installments: {average_installments:.2f}")


# ============================================================
# PAYMENT TYPE ANALYSIS
# ============================================================

payment_type_analysis = (
    payment_data
    .groupby("payment_type")
    .agg(
        payment_records=("payment_type", "count"),
        unique_orders=("order_id", "nunique"),
        total_payment_value=("payment_value", "sum"),
        average_payment_value=("payment_value", "mean"),
        median_payment_value=("payment_value", "median"),
        average_installments=("payment_installments", "mean")
    )
    .reset_index()
)

payment_type_analysis["revenue_percentage"] = (
    payment_type_analysis["total_payment_value"]
    / total_payment_value
    * 100
)

payment_type_analysis["order_percentage"] = (
    payment_type_analysis["unique_orders"]
    / unique_paid_orders
    * 100
)

payment_type_analysis[
    [
        "total_payment_value",
        "average_payment_value",
        "median_payment_value",
        "average_installments",
        "revenue_percentage",
        "order_percentage"
    ]
] = payment_type_analysis[
    [
        "total_payment_value",
        "average_payment_value",
        "median_payment_value",
        "average_installments",
        "revenue_percentage",
        "order_percentage"
    ]
].round(2)

payment_type_analysis = payment_type_analysis.sort_values(
    "total_payment_value",
    ascending=False
)

print("\n" + "=" * 70)
print("PAYMENT TYPE PERFORMANCE")
print("=" * 70)

print(payment_type_analysis.to_string(index=False))


# ============================================================
# INSTALLMENT ANALYSIS
# ============================================================

payment_installment_analysis = (
    payment_data
    .groupby("payment_installments")
    .agg(
        payment_records=("payment_installments", "count"),
        unique_orders=("order_id", "nunique"),
        total_payment_value=("payment_value", "sum"),
        average_payment_value=("payment_value", "mean")
    )
    .reset_index()
)

payment_installment_analysis["revenue_percentage"] = (
    payment_installment_analysis["total_payment_value"]
    / total_payment_value
    * 100
)

payment_installment_analysis[
    [
        "total_payment_value",
        "average_payment_value",
        "revenue_percentage"
    ]
] = payment_installment_analysis[
    [
        "total_payment_value",
        "average_payment_value",
        "revenue_percentage"
    ]
].round(2)

payment_installment_analysis = payment_installment_analysis.sort_values(
    "payment_installments"
)

print("\n" + "=" * 70)
print("INSTALLMENT ANALYSIS")
print("=" * 70)

print(payment_installment_analysis.to_string(index=False))


# ============================================================
# PAYMENT TYPE + INSTALLMENT ANALYSIS
# ============================================================

payment_type_installment = (
    payment_data
    .groupby(["payment_type", "payment_installments"])
    .agg(
        payment_records=("payment_type", "count"),
        total_payment_value=("payment_value", "sum"),
        average_payment_value=("payment_value", "mean")
    )
    .reset_index()
)

payment_type_installment[
    [
        "total_payment_value",
        "average_payment_value"
    ]
] = payment_type_installment[
    [
        "total_payment_value",
        "average_payment_value"
    ]
].round(2)


# ============================================================
# KEY BUSINESS FINDINGS
# ============================================================

top_revenue_payment = payment_type_analysis.iloc[0]

highest_average_payment = payment_type_analysis.loc[
    payment_type_analysis["average_payment_value"].idxmax()
]

most_installment_payment = payment_type_analysis.loc[
    payment_type_analysis["average_installments"].idxmax()
]

most_common_installment = payment_installment_analysis.loc[
    payment_installment_analysis["payment_records"].idxmax()
]

print("\n" + "=" * 70)
print("KEY PAYMENT INSIGHTS")
print("=" * 70)

print(
    f"Highest payment revenue method: "
    f"{top_revenue_payment['payment_type']}"
)

print(
    f"Highest average payment method: "
    f"{highest_average_payment['payment_type']}"
)

print(
    f"Payment method with highest average installments: "
    f"{most_installment_payment['payment_type']}"
)

print(
    f"Most common installment count: "
    f"{int(most_common_installment['payment_installments'])}"
)


# ============================================================
# CHART 1: PAYMENT TYPE REVENUE
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    payment_type_analysis["payment_type"],
    payment_type_analysis["total_payment_value"]
)

plt.title("Revenue by Payment Type")
plt.xlabel("Payment Type")
plt.ylabel("Total Payment Value")

plt.xticks(rotation=30)
plt.tight_layout()

plt.show()


# ============================================================
# CHART 2: INSTALLMENT DISTRIBUTION
# ============================================================

installment_chart = (
    payment_data["payment_installments"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(10, 6))

plt.bar(
    installment_chart.index.astype(str),
    installment_chart.values
)

plt.title("Payment Records by Installment Count")
plt.xlabel("Number of Installments")
plt.ylabel("Payment Records")

plt.tight_layout()

plt.show()


# ============================================================
# SAVE RESULTS
# ============================================================

payment_analysis = pd.DataFrame({
    "metric": [
        "total_payment_records",
        "unique_paid_orders",
        "total_payment_value",
        "average_payment_value",
        "median_payment_value",
        "average_installments"
    ],
    "value": [
        total_payment_records,
        unique_paid_orders,
        round(total_payment_value, 2),
        round(average_payment_value, 2),
        round(median_payment_value, 2),
        round(average_installments, 2)
    ]
})

payment_analysis.to_csv(
    PROCESSED_DATA / "payment_analysis.csv",
    index=False
)

payment_type_analysis.to_csv(
    PROCESSED_DATA / "payment_type_analysis.csv",
    index=False
)

payment_installment_analysis.to_csv(
    PROCESSED_DATA / "payment_installment_analysis.csv",
    index=False
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(
    PROCESSED_DATA / "payment_analysis.csv"
)

print(
    PROCESSED_DATA / "payment_type_analysis.csv"
)

print(
    PROCESSED_DATA / "payment_installment_analysis.csv"
)

print("\n" + "=" * 70)
print("STEP 7.12 COMPLETED")
print("=" * 70)