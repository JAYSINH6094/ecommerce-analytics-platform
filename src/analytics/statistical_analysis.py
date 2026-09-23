import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
# NUMERIC VARIABLES
# ============================================================

price = sales["price"]
freight = sales["freight_value"]


# ============================================================
# DESCRIPTIVE STATISTICS
# ============================================================

price_statistics = price.describe()

freight_statistics = freight.describe()


print("\n" + "=" * 70)
print("STATISTICAL ANALYSIS")
print("=" * 70)


print("\n" + "=" * 70)
print("PRICE DESCRIPTIVE STATISTICS")
print("=" * 70)

print(price_statistics)


print("\n" + "=" * 70)
print("FREIGHT VALUE DESCRIPTIVE STATISTICS")
print("=" * 70)

print(freight_statistics)


# ============================================================
# ADDITIONAL STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("ADDITIONAL STATISTICS")
print("=" * 70)


print(
    f"Price mean: "
    f"{np.mean(price):.2f}"
)

print(
    f"Price median: "
    f"{np.median(price):.2f}"
)

print(
    f"Price standard deviation: "
    f"{np.std(price):.2f}"
)

print(
    f"Freight mean: "
    f"{np.mean(freight):.2f}"
)

print(
    f"Freight median: "
    f"{np.median(freight):.2f}"
)

print(
    f"Freight standard deviation: "
    f"{np.std(freight):.2f}"
)


# ============================================================
# CORRELATION
# ============================================================

correlation = (
    sales[
        [
            "price",
            "freight_value"
        ]
    ]
    .corr()
)


print("\n" + "=" * 70)
print("PRICE VS FREIGHT CORRELATION")
print("=" * 70)

print(
    correlation
)


print(
    f"\nPearson correlation: "
    f"{correlation.loc['price', 'freight_value']:.4f}"
)


# ============================================================
# PRICE QUANTILES
# ============================================================

price_quantiles = (
    price.quantile(
        [
            0.25,
            0.50,
            0.75,
            0.90,
            0.95,
            0.99
        ]
    )
)


print("\n" + "=" * 70)
print("PRICE QUANTILES")
print("=" * 70)

print(price_quantiles)


# ============================================================
# OUTLIER THRESHOLD USING IQR
# ============================================================

Q1 = price.quantile(0.25)
Q3 = price.quantile(0.75)

IQR = Q3 - Q1

upper_bound = Q3 + (1.5 * IQR)

price_outliers = (
    price > upper_bound
).sum()


print("\n" + "=" * 70)
print("PRICE OUTLIER ANALYSIS")
print("=" * 70)

print(
    f"Q1: {Q1:.2f}"
)

print(
    f"Q3: {Q3:.2f}"
)

print(
    f"IQR: {IQR:.2f}"
)

print(
    f"Upper outlier threshold: "
    f"{upper_bound:.2f}"
)

print(
    f"Price observations above threshold: "
    f"{price_outliers:,}"
)


# ============================================================
# PRICE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    price,
    bins=50,
    kde=True
)

plt.title("Product Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()


# ============================================================
# FREIGHT DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    freight,
    bins=50,
    kde=True
)

plt.title("Freight Value Distribution")
plt.xlabel("Freight Value")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()


# ============================================================
# PRICE VS FREIGHT
# ============================================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=sales.sample(
        min(10000, len(sales)),
        random_state=42
    ),
    x="price",
    y="freight_value"
)

plt.title("Product Price vs Freight Value")
plt.xlabel("Price")
plt.ylabel("Freight Value")

plt.tight_layout()
plt.show()


# ============================================================
# SAVE STATISTICS
# ============================================================

statistics_output = (
    PROCESSED_DATA /
    "statistical_summary.csv"
)


statistics_table = pd.DataFrame(
    {
        "metric": [
            "price_mean",
            "price_median",
            "price_std",
            "freight_mean",
            "freight_median",
            "freight_std",
            "price_q1",
            "price_q3",
            "price_iqr",
            "price_upper_outlier_threshold",
            "price_outlier_count",
            "price_freight_correlation"
        ],
        "value": [
            np.mean(price),
            np.median(price),
            np.std(price),
            np.mean(freight),
            np.median(freight),
            np.std(freight),
            Q1,
            Q3,
            IQR,
            upper_bound,
            price_outliers,
            correlation.loc[
                "price",
                "freight_value"
            ]
        ]
    }
)


statistics_table.to_csv(
    statistics_output,
    index=False
)


print("\n" + "=" * 70)
print("FILE SAVED")
print("=" * 70)

print(statistics_output)


print("\n" + "=" * 70)
print("STEP 7.10 COMPLETED")
print("=" * 70)