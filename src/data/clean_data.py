from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "olist"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def load_data():
    print("Loading raw datasets...")

    data = {
        "customers": pd.read_csv(
            RAW_DATA_DIR / "olist_customers_dataset.csv"
        ),
        "geolocation": pd.read_csv(
            RAW_DATA_DIR / "olist_geolocation_dataset.csv"
        ),
        "orders": pd.read_csv(
            RAW_DATA_DIR / "olist_orders_dataset.csv"
        ),
        "order_items": pd.read_csv(
            RAW_DATA_DIR / "olist_order_items_dataset.csv"
        ),
        "payments": pd.read_csv(
            RAW_DATA_DIR / "olist_order_payments_dataset.csv"
        ),
        "reviews": pd.read_csv(
            RAW_DATA_DIR / "olist_order_reviews_dataset.csv"
        ),
        "products": pd.read_csv(
            RAW_DATA_DIR / "olist_products_dataset.csv"
        ),
        "sellers": pd.read_csv(
            RAW_DATA_DIR / "olist_sellers_dataset.csv"
        ),
        "category_translation": pd.read_csv(
            RAW_DATA_DIR / "product_category_name_translation.csv"
        ),
    }

    return data


def clean_orders(df):
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df


def clean_order_items(df):
    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"],
        errors="coerce"
    )

    return df


def clean_reviews(df):
    df["review_creation_date"] = pd.to_datetime(
        df["review_creation_date"],
        errors="coerce"
    )

    df["review_answer_timestamp"] = pd.to_datetime(
        df["review_answer_timestamp"],
        errors="coerce"
    )

    return df


def clean_geolocation(df):
    before = len(df)

    df = df.drop_duplicates().copy()

    after = len(df)

    print(
        f"Geolocation duplicates removed: "
        f"{before - after:,}"
    )

    return df


def clean_products(df):
    category_columns = [
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
    ]

    # Products remain in the dataset.
    # Missing category will be handled as Unknown.
    df["product_category_name"] = (
        df["product_category_name"]
        .fillna("Unknown")
    )

    # Physical attributes remain NULL where unavailable.
    for column in [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


def clean_data():
    data = load_data()

    print("\nCleaning datasets...")

    data["orders"] = clean_orders(data["orders"])
    data["order_items"] = clean_order_items(
        data["order_items"]
    )
    data["reviews"] = clean_reviews(
        data["reviews"]
    )
    data["geolocation"] = clean_geolocation(
        data["geolocation"]
    )
    data["products"] = clean_products(
        data["products"]
    )

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\nSaving processed datasets...")

    for name, df in data.items():
        output_file = (
            PROCESSED_DATA_DIR /
            f"{name}.csv"
        )

        df.to_csv(
            output_file,
            index=False
        )

        print(
            f"{name:20} "
            f"{len(df):,} rows saved"
        )

    print("\n" + "=" * 80)
    print("DATA CLEANING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    clean_data()