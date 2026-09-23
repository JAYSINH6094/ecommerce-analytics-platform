from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "olist"


def load_table(filename):
    return pd.read_csv(RAW_DATA_DIR / filename)


def profile_business_fields():
    orders = load_table("olist_orders_dataset.csv")
    items = load_table("olist_order_items_dataset.csv")
    payments = load_table("olist_order_payments_dataset.csv")
    reviews = load_table("olist_order_reviews_dataset.csv")
    products = load_table("olist_products_dataset.csv")

    print("=" * 80)
    print("BUSINESS FIELD PROFILING")
    print("=" * 80)

    # ---------------------------------------------------------
    # ORDERS
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("ORDER STATUS")
    print("=" * 80)
    print(orders["order_status"].value_counts(dropna=False))

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    print("\nORDER PURCHASE DATE RANGE")
    print(f"Start: {orders['order_purchase_timestamp'].min()}")
    print(f"End  : {orders['order_purchase_timestamp'].max()}")

    # ---------------------------------------------------------
    # ORDER ITEMS
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("ORDER ITEM NUMERIC FIELDS")
    print("=" * 80)

    print("\nPrice:")
    print(items["price"].describe())

    print("\nFreight Value:")
    print(items["freight_value"].describe())

    # ---------------------------------------------------------
    # PAYMENTS
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("PAYMENT TYPES")
    print("=" * 80)
    print(payments["payment_type"].value_counts(dropna=False))

    print("\nPayment Value:")
    print(payments["payment_value"].describe())

    # ---------------------------------------------------------
    # REVIEWS
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("REVIEW SCORES")
    print("=" * 80)
    print(reviews["review_score"].value_counts().sort_index())

    # ---------------------------------------------------------
    # PRODUCTS
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("PRODUCT CATEGORIES")
    print("=" * 80)

    print(
        f"Unique product categories: "
        f"{products['product_category_name'].nunique(dropna=True)}"
    )

    print("\nTop 15 categories by product count:")
    print(
        products["product_category_name"]
        .value_counts()
        .head(15)
    )

    print("\n" + "=" * 80)
    print("BUSINESS FIELD PROFILING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    profile_business_fields()