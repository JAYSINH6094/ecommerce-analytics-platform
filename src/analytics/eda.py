import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


# ============================================================
# LOAD PROCESSED DATA
# ============================================================

customers = pd.read_csv(PROCESSED_DATA / "customers.csv")
geolocation = pd.read_csv(PROCESSED_DATA / "geolocation.csv")
orders = pd.read_csv(PROCESSED_DATA / "orders.csv")
order_items = pd.read_csv(PROCESSED_DATA / "order_items.csv")
payments = pd.read_csv(PROCESSED_DATA / "payments.csv")
reviews = pd.read_csv(PROCESSED_DATA / "reviews.csv")
products = pd.read_csv(PROCESSED_DATA / "products.csv")
sellers = pd.read_csv(PROCESSED_DATA / "sellers.csv")
category_translation = pd.read_csv(
    PROCESSED_DATA / "category_translation.csv"
)


# ============================================================
# DATASET SUMMARY
# ============================================================

datasets = {
    "customers": customers,
    "geolocation": geolocation,
    "orders": orders,
    "order_items": order_items,
    "payments": payments,
    "reviews": reviews,
    "products": products,
    "sellers": sellers,
    "category_translation": category_translation,
}


print("\n" + "=" * 70)
print("PROCESSED DATASET SUMMARY")
print("=" * 70)

for name, df in datasets.items():
    print(f"{name:25} -> {df.shape[0]:>10,} rows × {df.shape[1]} columns")


# ============================================================
# COLUMN INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("ORDERS DATASET")
print("=" * 70)

print(orders.head())

print("\nColumns:")
print(orders.columns.tolist())

print("\nData Types:")
print(orders.dtypes)


# ============================================================
# BASIC DATA QUALITY CHECK
# ============================================================

print("\n" + "=" * 70)
print("BASIC DATA QUALITY CHECK")
print("=" * 70)

print("\nOrders missing values:")
print(orders.isnull().sum())

print("\nOrder items missing values:")
print(order_items.isnull().sum())

print("\nProducts missing values:")
print(products.isnull().sum())


print("\n" + "=" * 70)
print("EDA STEP 7.1 COMPLETED")
print("=" * 70)