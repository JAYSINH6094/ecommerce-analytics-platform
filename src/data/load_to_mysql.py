from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DB_USER = "root"
DB_PASSWORD = "6094"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "ecommerce_analytics"


DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# =========================================================
# TABLE LOAD ORDER
# =========================================================

TABLES = [
    ("customers.csv", "customers"),
    ("sellers.csv", "sellers"),
    ("products.csv", "products"),
    ("category_translation.csv", "category_translation"),
    ("orders.csv", "orders"),
    ("order_items.csv", "order_items"),
    ("payments.csv", "payments"),
    ("reviews.csv", "reviews"),
    ("geolocation.csv", "geolocation"),
]


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    print("=" * 80)
    print("MYSQL DATA LOADING")
    print("=" * 80)

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )

    # Test connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("\nMySQL connection successful.")

    for filename, table_name in TABLES:

        file_path = PROCESSED_DATA_DIR / filename

        print("\n" + "-" * 80)
        print(f"Loading: {filename}")
        print(f"Target : {table_name}")
        print("-" * 80)

        df = pd.read_csv(file_path)

        print(f"Rows to load: {len(df):,}")

        # Convert pandas NaN to Python None
        # so MySQL receives proper NULL values.
        df = df.where(pd.notna(df), None)

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=5000,
            method="multi"
        )

        print(f"Loaded successfully: {len(df):,} rows")

    print("\n" + "=" * 80)
    print("MYSQL DATA LOADING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    load_data()