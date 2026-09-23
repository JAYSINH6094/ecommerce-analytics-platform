from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


EXPECTED_FILES = [
    "customers.csv",
    "geolocation.csv",
    "orders.csv",
    "order_items.csv",
    "payments.csv",
    "reviews.csv",
    "products.csv",
    "sellers.csv",
    "category_translation.csv",
]


def validate_processed_data():
    print("=" * 80)
    print("PROCESSED DATA VALIDATION")
    print("=" * 80)

    validation_passed = True

    for filename in EXPECTED_FILES:
        file_path = PROCESSED_DATA_DIR / filename

        print(f"\nChecking: {filename}")

        # File existence
        if not file_path.exists():
            print("  FAIL: File does not exist.")
            validation_passed = False
            continue

        df = pd.read_csv(file_path)

        # Empty dataset check
        if df.empty:
            print("  FAIL: Dataset is empty.")
            validation_passed = False
        else:
            print(f"  Rows: {len(df):,}")
            print(f"  Columns: {len(df.columns)}")

        # Duplicate check
        duplicates = df.duplicated().sum()

        if duplicates > 0:
            print(f"  WARNING: {duplicates:,} duplicate rows found.")
        else:
            print("  Duplicate rows: 0")

        # Column-level missing values
        missing_cells = df.isnull().sum().sum()

        print(f"  Missing cells: {missing_cells:,}")

    # ---------------------------------------------------------
    # Business key validation
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("BUSINESS KEY VALIDATION")
    print("=" * 80)

    customers = pd.read_csv(
        PROCESSED_DATA_DIR / "customers.csv"
    )

    orders = pd.read_csv(
        PROCESSED_DATA_DIR / "orders.csv"
    )

    products = pd.read_csv(
        PROCESSED_DATA_DIR / "products.csv"
    )

    sellers = pd.read_csv(
        PROCESSED_DATA_DIR / "sellers.csv"
    )

    key_checks = {
        "customer_id": customers["customer_id"],
        "order_id": orders["order_id"],
        "product_id": products["product_id"],
        "seller_id": sellers["seller_id"],
    }

    for key_name, series in key_checks.items():

        null_count = series.isnull().sum()
        duplicate_count = series.duplicated().sum()

        print(f"\n{key_name}")
        print(f"  NULL values      : {null_count:,}")
        print(f"  Duplicate values : {duplicate_count:,}")

        if null_count > 0 or duplicate_count > 0:
            validation_passed = False
            print("  FAIL")
        else:
            print("  PASS")

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    print("\n" + "=" * 80)

    if validation_passed:
        print("VALIDATION RESULT: PASSED")
        print("Processed data is ready for the database stage.")
    else:
        print("VALIDATION RESULT: REVIEW REQUIRED")
        print("One or more validation checks failed.")

    print("=" * 80)


if __name__ == "__main__":
    validate_processed_data()