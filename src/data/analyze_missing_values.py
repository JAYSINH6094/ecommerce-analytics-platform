from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "olist"


def load_table(filename):
    return pd.read_csv(RAW_DATA_DIR / filename)


def analyze_missing_values():
    orders = load_table("olist_orders_dataset.csv")
    products = load_table("olist_products_dataset.csv")
    reviews = load_table("olist_order_reviews_dataset.csv")

    print("=" * 80)
    print("MISSING VALUE BUSINESS ANALYSIS")
    print("=" * 80)

    # ---------------------------------------------------------
    # ORDERS
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("ORDERS")
    print("=" * 80)

    print("\nMissing values by order status:")

    missing_columns = [
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
    ]

    for column in missing_columns:
        print(f"\n{column}:")
        print(
            orders.loc[
                orders[column].isna(),
                "order_status"
            ].value_counts()
        )

    # ---------------------------------------------------------
    # PRODUCTS
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("PRODUCTS")
    print("=" * 80)

    print("\nMissing values by column:")

    product_missing = products.isna().sum()
    print(product_missing[product_missing > 0])

    print("\nRows with missing product category:")

    missing_category = products[
        products["product_category_name"].isna()
    ]

    print(f"Count: {len(missing_category):,}")

    print(
        missing_category[
            [
                "product_id",
                "product_category_name",
                "product_name_lenght",
                "product_description_lenght",
                "product_photos_qty",
                "product_weight_g",
                "product_length_cm",
                "product_height_cm",
                "product_width_cm",
            ]
        ].head(10).to_string(index=False)
    )

    # ---------------------------------------------------------
    # REVIEWS
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("REVIEWS")
    print("=" * 80)

    print("\nMissing review fields:")
    review_missing = reviews.isna().sum()
    print(review_missing[review_missing > 0])

    print("\nReview comment availability:")

    review_comment_summary = pd.DataFrame(
        {
            "review_score": sorted(reviews["review_score"].unique()),
            "total_reviews": [
                (reviews["review_score"] == score).sum()
                for score in sorted(reviews["review_score"].unique())
            ],
            "missing_message": [
                reviews.loc[
                    reviews["review_score"] == score,
                    "review_comment_message"
                ].isna().sum()
                for score in sorted(reviews["review_score"].unique())
            ],
        }
    )

    print(review_comment_summary.to_string(index=False))

    print("\n" + "=" * 80)
    print("MISSING VALUE ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    analyze_missing_values()