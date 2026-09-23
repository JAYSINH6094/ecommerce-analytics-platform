import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


# ============================================================
# HELPERS
# ============================================================

passed = 0
failed = 0


def check(name, condition, details=""):
    global passed, failed

    if condition:
        print(f"[PASS] {name}")
        if details:
            print(f"       {details}")
        passed += 1
    else:
        print(f"[FAIL] {name}")
        if details:
            print(f"       {details}")
        failed += 1


# ============================================================
# LOAD CORE DATA
# ============================================================

customers = pd.read_csv(PROCESSED_DATA / "customers.csv")
orders = pd.read_csv(PROCESSED_DATA / "orders.csv")
order_items = pd.read_csv(PROCESSED_DATA / "order_items.csv")
payments = pd.read_csv(PROCESSED_DATA / "payments.csv")
reviews = pd.read_csv(PROCESSED_DATA / "reviews.csv")
products = pd.read_csv(PROCESSED_DATA / "products.csv")
sellers = pd.read_csv(PROCESSED_DATA / "sellers.csv")

sales = pd.read_csv(
    PROCESSED_DATA / "analysis_ready_sales.csv"
)

monthly_sales = pd.read_csv(
    PROCESSED_DATA / "monthly_sales_analysis.csv"
)

customer_behavior = pd.read_csv(
    PROCESSED_DATA / "customer_behavior_analysis.csv"
)

seller_analysis = pd.read_csv(
    PROCESSED_DATA / "seller_analysis.csv"
)

order_basket = pd.read_csv(
    PROCESSED_DATA / "order_basket_analysis.csv"
)


# ============================================================
# SECTION 1: CORE DATASET VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("1. CORE DATASET VALIDATION")
print("=" * 70)

check(
    "Customers have unique customer IDs",
    customers["customer_id"].is_unique,
    f"Rows: {len(customers):,}"
)

check(
    "Orders have unique order IDs",
    orders["order_id"].is_unique,
    f"Rows: {len(orders):,}"
)

check(
    "Products have unique product IDs",
    products["product_id"].is_unique,
    f"Rows: {len(products):,}"
)

check(
    "Sellers have unique seller IDs",
    sellers["seller_id"].is_unique,
    f"Rows: {len(sellers):,}"
)

check(
    "Order items contain no missing order IDs",
    order_items["order_id"].notna().all()
)

check(
    "Order items contain no missing product IDs",
    order_items["product_id"].notna().all()
)

check(
    "Order items contain no missing seller IDs",
    order_items["seller_id"].notna().all()
)


# ============================================================
# SECTION 2: ORDER STATUS VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("2. ORDER STATUS VALIDATION")
print("=" * 70)

delivered_orders = orders[
    orders["order_status"] == "delivered"
]

delivered_order_count = delivered_orders[
    "order_id"
].nunique()

check(
    "Delivered order count matches expected analytical population",
    delivered_order_count == 96478,
    f"Delivered orders: {delivered_order_count:,}"
)

check(
    "Analysis-ready sales contains only delivered orders",
    sales["order_id"].isin(
        delivered_orders["order_id"]
    ).all()
)

check(
    "Analysis-ready sales contains 96,478 unique delivered orders",
    sales["order_id"].nunique() == 96478,
    f"Unique orders: {sales['order_id'].nunique():,}"
)


# ============================================================
# SECTION 3: REVENUE CONSISTENCY
# ============================================================

print("\n" + "=" * 70)
print("3. REVENUE CONSISTENCY")
print("=" * 70)

item_revenue = order_items[
    order_items["order_id"].isin(
        delivered_orders["order_id"]
    )
]["price"].sum()

analysis_revenue = sales["revenue"].sum()

revenue_difference = abs(
    item_revenue - analysis_revenue
)

check(
    "Analysis revenue matches delivered order-item revenue",
    revenue_difference < 0.01,
    f"Difference: {revenue_difference:.4f}"
)

print(
    f"Delivered item revenue: {item_revenue:,.2f}"
)

print(
    f"Analysis-ready revenue: {analysis_revenue:,.2f}"
)


# ============================================================
# SECTION 4: ORDER ITEM CONSISTENCY
# ============================================================

print("\n" + "=" * 70)
print("4. ORDER ITEM CONSISTENCY")
print("=" * 70)

delivered_items = order_items[
    order_items["order_id"].isin(
        delivered_orders["order_id"]
    )
]

delivered_item_count = len(delivered_items)

analysis_item_count = len(sales)

check(
    "Analysis-ready item count matches delivered order items",
    delivered_item_count == analysis_item_count,
    f"Delivered items: {delivered_item_count:,} | "
    f"Analysis items: {analysis_item_count:,}"
)

check(
    "No negative product prices",
    (order_items["price"] >= 0).all()
)

check(
    "No negative freight values",
    (order_items["freight_value"] >= 0).all()
)


# ============================================================
# SECTION 5: PAYMENT VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("5. PAYMENT VALIDATION")
print("=" * 70)

delivered_payment_orders = payments[
    payments["order_id"].isin(
        delivered_orders["order_id"]
    )
]["order_id"].nunique()

check(
    "Most delivered orders have payment records",
    delivered_payment_orders >= 96400,
    f"Delivered orders with payments: "
    f"{delivered_payment_orders:,}"
)

check(
    "No negative payment values",
    (payments["payment_value"] >= 0).all()
)

check(
    "Payment installments are non-negative",
    (payments["payment_installments"] >= 0).all()
)


# ============================================================
# SECTION 6: CUSTOMER ANALYTICS VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("6. CUSTOMER ANALYTICS VALIDATION")
print("=" * 70)

customer_count = (
    sales["customer_unique_id"]
    .nunique()
)

behavior_customer_count = (
    customer_behavior["customer_unique_id"]
    .nunique()
)

check(
    "Customer count matches analysis-ready sales",
    customer_count == behavior_customer_count,
    f"Sales customers: {customer_count:,} | "
    f"Behavior customers: {behavior_customer_count:,}"
)

check(
    "Customer behavior has one row per customer",
    customer_behavior["customer_unique_id"].is_unique
)


# ============================================================
# SECTION 7: SELLER ANALYTICS VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("7. SELLER ANALYTICS VALIDATION")
print("=" * 70)

seller_count = (
    sales["seller_id"]
    .nunique()
)

seller_analysis_count = (
    seller_analysis["seller_id"]
    .nunique()
)

check(
    "Seller count matches analysis-ready sales",
    seller_count == seller_analysis_count,
    f"Sales sellers: {seller_count:,} | "
    f"Seller analysis sellers: {seller_analysis_count:,}"
)

check(
    "Seller analysis has one row per seller",
    seller_analysis["seller_id"].is_unique
)

seller_revenue = seller_analysis[
    "total_revenue"
].sum()

check(
    "Seller revenue matches total analysis revenue",
    abs(seller_revenue - analysis_revenue) < 0.01,
    f"Difference: "
    f"{abs(seller_revenue - analysis_revenue):.4f}"
)


# ============================================================
# SECTION 8: BASKET ANALYTICS VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("8. BASKET ANALYTICS VALIDATION")
print("=" * 70)

basket_order_count = (
    order_basket["order_id"]
    .nunique()
)

check(
    "Basket analysis has one row per delivered order",
    basket_order_count == delivered_order_count,
    f"Basket orders: {basket_order_count:,}"
)

basket_item_count = (
    order_basket["item_count"].sum()
)

check(
    "Basket item count matches delivered item count",
    basket_item_count == delivered_item_count,
    f"Basket items: {basket_item_count:,}"
)

basket_revenue = (
    order_basket["basket_revenue"].sum()
)

check(
    "Basket revenue matches total analysis revenue",
    abs(basket_revenue - analysis_revenue) < 0.01,
    f"Difference: "
    f"{abs(basket_revenue - analysis_revenue):.4f}"
)


# ============================================================
# SECTION 9: MONTHLY SALES VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("9. MONTHLY SALES VALIDATION")
print("=" * 70)

monthly_revenue = (
    monthly_sales["revenue"].sum()
)

check(
    "Monthly revenue matches total analysis revenue",
    abs(monthly_revenue - analysis_revenue) < 0.01,
    f"Difference: "
    f"{abs(monthly_revenue - analysis_revenue):.4f}"
)

monthly_orders = (
    monthly_sales["orders"]
    .sum()
)

check(
    "Monthly order counts match delivered order count",
    monthly_orders == delivered_order_count,
    f"Monthly orders: {monthly_orders:,}"
)


# ============================================================
# SECTION 10: DATA QUALITY CHECKS
# ============================================================

print("\n" + "=" * 70)
print("10. DATA QUALITY CHECKS")
print("=" * 70)

check(
    "No duplicate customer IDs",
    customers["customer_id"].duplicated().sum() == 0
)

check(
    "No duplicate order IDs",
    orders["order_id"].duplicated().sum() == 0
)

check(
    "No duplicate product IDs",
    products["product_id"].duplicated().sum() == 0
)

check(
    "No duplicate seller IDs",
    sellers["seller_id"].duplicated().sum() == 0
)

check(
    "Analysis-ready sales contains no missing order IDs",
    sales["order_id"].notna().all()
)

check(
    "Analysis-ready sales contains no missing customer IDs",
    sales["customer_unique_id"].notna().all()
)

check(
    "Analysis-ready sales contains no missing seller IDs",
    sales["seller_id"].notna().all()
)


# ============================================================
# SECTION 11: FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL VALIDATION SUMMARY")
print("=" * 70)

print(f"Checks passed: {passed}")
print(f"Checks failed: {failed}")

if failed == 0:
    print("\nVALIDATION RESULT: PASSED")
else:
    print("\nVALIDATION RESULT: REVIEW REQUIRED")