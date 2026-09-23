import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


# ============================================================
# LOAD DATA
# ============================================================

orders = pd.read_csv(PROCESSED_DATA / "orders.csv")
order_items = pd.read_csv(PROCESSED_DATA / "order_items.csv")
products = pd.read_csv(PROCESSED_DATA / "products.csv")
category_translation = pd.read_csv(
    PROCESSED_DATA / "category_translation.csv"
)
customers = pd.read_csv(PROCESSED_DATA / "customers.csv")


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
# FILTER DELIVERED ORDERS
# ============================================================

delivered_orders = orders[
    orders["order_status"] == "delivered"
].copy()


print("\n" + "=" * 70)
print("DELIVERED ORDERS")
print("=" * 70)

print(f"Delivered orders: {len(delivered_orders):,}")


# ============================================================
# JOIN ORDERS WITH ORDER ITEMS
# ============================================================

sales = delivered_orders.merge(
    order_items,
    on="order_id",
    how="inner"
)


# ============================================================
# JOIN PRODUCTS
# ============================================================

sales = sales.merge(
    products[
        [
            "product_id",
            "product_category_name"
        ]
    ],
    on="product_id",
    how="left"
)


# ============================================================
# JOIN CATEGORY TRANSLATION
# ============================================================

sales = sales.merge(
    category_translation,
    on="product_category_name",
    how="left"
)


# ============================================================
# JOIN CUSTOMERS
# ============================================================

sales = sales.merge(
    customers[
        [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state"
        ]
    ],
    on="customer_id",
    how="left"
)


# ============================================================
# HANDLE UNKNOWN CATEGORY
# ============================================================

sales["product_category_name_english"] = (
    sales["product_category_name_english"]
    .fillna("Unknown")
)


# ============================================================
# CREATE ANALYTICAL COLUMNS
# ============================================================

sales["order_month"] = (
    sales["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

sales["order_year"] = (
    sales["order_purchase_timestamp"]
    .dt.year
)

sales["order_month_number"] = (
    sales["order_purchase_timestamp"]
    .dt.month
)

sales["revenue"] = sales["price"]

sales["total_item_value"] = (
    sales["price"] + sales["freight_value"]
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n" + "=" * 70)
print("ANALYSIS-READY SALES DATASET")
print("=" * 70)

print(f"Rows: {len(sales):,}")
print(f"Columns: {len(sales.columns)}")

print("\nColumns:")
print(sales.columns.tolist())

print("\nFirst 5 rows:")
print(sales.head())


# ============================================================
# BASIC VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION")
print("=" * 70)

print(
    "Unique orders:",
    sales["order_id"].nunique()
)

print(
    "Unique customers:",
    sales["customer_unique_id"].nunique()
)

print(
    "Unique products:",
    sales["product_id"].nunique()
)

print(
    "Total revenue:",
    round(sales["revenue"].sum(), 2)
)

print(
    "Total freight:",
    round(sales["freight_value"].sum(), 2)
)

print("\nMissing values:")
print(
    sales[
        [
            "product_category_name_english",
            "customer_city",
            "customer_state"
        ]
    ].isnull().sum()
)


# ============================================================
# SAVE ANALYSIS-READY DATASET
# ============================================================

OUTPUT_FILE = (
    PROCESSED_DATA /
    "analysis_ready_sales.csv"
)

sales.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("STEP 7.2 COMPLETED")
print("=" * 70)