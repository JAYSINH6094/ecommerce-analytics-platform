import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "ecommerce_analytics")

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/"
    f"{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


# ---------------------------------------------------------
# Historical Analytics
# ---------------------------------------------------------

def get_historical_metrics():
    """
    Load historical analytics metrics from the real Olist dataset.
    """

    sales_path = os.path.join(
        PROCESSED_DIR,
        "analysis_ready_sales.csv"
    )

    sales = pd.read_csv(sales_path)

    sales["revenue"] = pd.to_numeric(
        sales["revenue"],
        errors="coerce"
    )

    historical_revenue = sales["revenue"].sum()

    historical_orders = sales["order_id"].nunique()

    historical_items = len(sales)

    historical_customers = sales[
        "customer_unique_id"
    ].nunique()

    historical_aov = (
        historical_revenue / historical_orders
        if historical_orders > 0
        else 0
    )

    return {
        "historical_revenue": historical_revenue,
        "historical_orders": historical_orders,
        "historical_items": historical_items,
        "historical_customers": historical_customers,
        "historical_aov": historical_aov
    }


# ---------------------------------------------------------
# Real-Time Analytics
# ---------------------------------------------------------

def get_realtime_metrics():
    """
    Calculate current real-time metrics
    from the realtime_orders table.
    """

    query = text("""
        SELECT
            COUNT(DISTINCT order_id) AS realtime_orders,
            COALESCE(SUM(price * quantity), 0) AS realtime_revenue,
            COALESCE(SUM(quantity), 0) AS realtime_items
        FROM realtime_orders
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()

    realtime_orders = int(result["realtime_orders"] or 0)
    realtime_revenue = float(result["realtime_revenue"] or 0)
    realtime_items = int(result["realtime_items"] or 0)

    realtime_aov = (
        realtime_revenue / realtime_orders
        if realtime_orders > 0
        else 0
    )

    return {
        "realtime_revenue": realtime_revenue,
        "realtime_orders": realtime_orders,
        "realtime_items": realtime_items,
        "realtime_aov": realtime_aov
    }


# ---------------------------------------------------------
# Today's Real-Time Analytics
# ---------------------------------------------------------

def get_today_metrics():
    """
    Calculate today's real-time order activity.
    """

    query = text("""
        SELECT
            COUNT(DISTINCT order_id) AS today_orders,
            COALESCE(SUM(price * quantity), 0) AS today_revenue,
            COALESCE(SUM(quantity), 0) AS today_items
        FROM realtime_orders
        WHERE DATE(order_timestamp) = CURDATE()
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()

    today_orders = int(result["today_orders"] or 0)
    today_revenue = float(result["today_revenue"] or 0)
    today_items = int(result["today_items"] or 0)

    today_aov = (
        today_revenue / today_orders
        if today_orders > 0
        else 0
    )

    return {
        "today_revenue": today_revenue,
        "today_orders": today_orders,
        "today_items": today_items,
        "today_aov": today_aov
    }


# ---------------------------------------------------------
# Combined Analytics
# ---------------------------------------------------------

def get_combined_metrics():
    """
    Combine historical Olist analytics
    with real-time operational data.

    Historical data remains unchanged.
    Real-time data is treated as a separate
    operational stream.
    """

    historical = get_historical_metrics()
    realtime = get_realtime_metrics()
    today = get_today_metrics()

    combined_revenue = (
        historical["historical_revenue"]
        + realtime["realtime_revenue"]
    )

    combined_orders = (
        historical["historical_orders"]
        + realtime["realtime_orders"]
    )

    combined_items = (
        historical["historical_items"]
        + realtime["realtime_items"]
    )

    combined_aov = (
        combined_revenue / combined_orders
        if combined_orders > 0
        else 0
    )

    return {
        **historical,
        **realtime,
        **today,
        "combined_revenue": combined_revenue,
        "combined_orders": combined_orders,
        "combined_items": combined_items,
        "combined_aov": combined_aov
    }


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("UNIFIED E-COMMERCE ANALYTICS")
    print("=" * 60)

    metrics = get_combined_metrics()

    print("\n--- HISTORICAL ANALYTICS ---")
    print(
        f"Historical Revenue   : "
        f"{metrics['historical_revenue']:,.2f}"
    )
    print(
        f"Historical Orders    : "
        f"{metrics['historical_orders']:,}"
    )
    print(
        f"Historical Items     : "
        f"{metrics['historical_items']:,}"
    )
    print(
        f"Historical Customers : "
        f"{metrics['historical_customers']:,}"
    )
    print(
        f"Historical AOV       : "
        f"{metrics['historical_aov']:,.2f}"
    )

    print("\n--- REAL-TIME ANALYTICS ---")
    print(
        f"Real-Time Revenue    : "
        f"{metrics['realtime_revenue']:,.2f}"
    )
    print(
        f"Real-Time Orders     : "
        f"{metrics['realtime_orders']:,}"
    )
    print(
        f"Real-Time Items      : "
        f"{metrics['realtime_items']:,}"
    )
    print(
        f"Real-Time AOV        : "
        f"{metrics['realtime_aov']:,.2f}"
    )

    print("\n--- TODAY'S ACTIVITY ---")
    print(
        f"Today's Revenue      : "
        f"{metrics['today_revenue']:,.2f}"
    )
    print(
        f"Today's Orders       : "
        f"{metrics['today_orders']:,}"
    )
    print(
        f"Today's Items        : "
        f"{metrics['today_items']:,}"
    )
    print(
        f"Today's AOV          : "
        f"{metrics['today_aov']:,.2f}"
    )

    print("\n--- COMBINED ANALYTICS ---")
    print(
        f"Combined Revenue     : "
        f"{metrics['combined_revenue']:,.2f}"
    )
    print(
        f"Combined Orders      : "
        f"{metrics['combined_orders']:,}"
    )
    print(
        f"Combined Items       : "
        f"{metrics['combined_items']:,}"
    )
    print(
        f"Combined AOV         : "
        f"{metrics['combined_aov']:,.2f}"
    )

    print("\n" + "=" * 60)
    print("UNIFIED ANALYTICS TEST COMPLETED")
    print("=" * 60)