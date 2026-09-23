from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "olist"


def load_table(filename):
    return pd.read_csv(RAW_DATA_DIR / filename)


def check_relationships():
    customers = load_table("olist_customers_dataset.csv")
    orders = load_table("olist_orders_dataset.csv")
    items = load_table("olist_order_items_dataset.csv")
    products = load_table("olist_products_dataset.csv")
    sellers = load_table("olist_sellers_dataset.csv")
    payments = load_table("olist_order_payments_dataset.csv")
    reviews = load_table("olist_order_reviews_dataset.csv")

    print("=" * 80)
    print("OLIST TABLE RELATIONSHIP ANALYSIS")
    print("=" * 80)

    # Orders -> Customers
    order_customer_match = orders["customer_id"].isin(
        customers["customer_id"]
    ).mean() * 100

    print("\n1. ORDERS -> CUSTOMERS")
    print(f"Orders with matching customer: {order_customer_match:.2f}%")

    # Order Items -> Orders
    item_order_match = items["order_id"].isin(
        orders["order_id"]
    ).mean() * 100

    print("\n2. ORDER ITEMS -> ORDERS")
    print(f"Items with matching order: {item_order_match:.2f}%")

    # Order Items -> Products
    item_product_match = items["product_id"].isin(
        products["product_id"]
    ).mean() * 100

    print("\n3. ORDER ITEMS -> PRODUCTS")
    print(f"Items with matching product: {item_product_match:.2f}%")

    # Order Items -> Sellers
    item_seller_match = items["seller_id"].isin(
        sellers["seller_id"]
    ).mean() * 100

    print("\n4. ORDER ITEMS -> SELLERS")
    print(f"Items with matching seller: {item_seller_match:.2f}%")

    # Payments -> Orders
    payment_order_match = payments["order_id"].isin(
        orders["order_id"]
    ).mean() * 100

    print("\n5. PAYMENTS -> ORDERS")
    print(f"Payments with matching order: {payment_order_match:.2f}%")

    # Reviews -> Orders
    review_order_match = reviews["order_id"].isin(
        orders["order_id"]
    ).mean() * 100

    print("\n6. REVIEWS -> ORDERS")
    print(f"Reviews with matching order: {review_order_match:.2f}%")

    # Uniqueness checks
    print("\n" + "=" * 80)
    print("KEY UNIQUENESS CHECKS")
    print("=" * 80)

    print(f"\nUnique customer_id: {customers['customer_id'].nunique():,}")
    print(f"Customer rows      : {len(customers):,}")

    print(f"\nUnique order_id: {orders['order_id'].nunique():,}")
    print(f"Order rows      : {len(orders):,}")

    print(f"\nUnique product_id: {products['product_id'].nunique():,}")
    print(f"Product rows     : {len(products):,}")

    print(f"\nUnique seller_id: {sellers['seller_id'].nunique():,}")
    print(f"Seller rows     : {len(sellers):,}")

    print("\n" + "=" * 80)
    print("RELATIONSHIP ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    check_relationships()