import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


# ============================================================
# LOAD ANALYTICAL DATA
# ============================================================

sales = pd.read_csv(
    PROCESSED_DATA / "analysis_ready_sales.csv"
)

customers = pd.read_csv(
    PROCESSED_DATA / "customer_behavior_analysis.csv"
)

rfm = pd.read_csv(
    PROCESSED_DATA / "rfm_dashboard.csv"
)

delivery = pd.read_csv(
    PROCESSED_DATA / "delivery_analysis.csv"
)

payments = pd.read_csv(
    PROCESSED_DATA / "payment_analysis.csv"
)

basket = pd.read_csv(
    PROCESSED_DATA / "order_basket_analysis.csv"
)

reviews = pd.read_csv(
    PROCESSED_DATA / "review_analysis.csv"
)

seller = pd.read_csv(
    PROCESSED_DATA / "seller_analysis.csv"
)

category_analysis = pd.read_csv(
    PROCESSED_DATA / "category_analysis.csv"
)

regional_analysis = pd.read_csv(
    PROCESSED_DATA / "regional_analysis.csv"
)


# ============================================================
# BASIC DATA TYPE CONVERSIONS
# ============================================================

sales["revenue"] = pd.to_numeric(
    sales["revenue"],
    errors="coerce"
)

sales["freight_value"] = pd.to_numeric(
    sales["freight_value"],
    errors="coerce"
)

delivery["delivery_days"] = pd.to_numeric(
    delivery["delivery_days"],
    errors="coerce"
)

delivery["delivery_delay_days"] = pd.to_numeric(
    delivery["delivery_delay_days"],
    errors="coerce"
)

reviews["review_score"] = pd.to_numeric(
    reviews["review_score"],
    errors="coerce"
)

reviews["review_count"] = pd.to_numeric(
    reviews["review_count"],
    errors="coerce"
)

payments["value"] = pd.to_numeric(
    payments["value"],
    errors="coerce"
)

basket["basket_revenue"] = pd.to_numeric(
    basket["basket_revenue"],
    errors="coerce"
)

basket["item_count"] = pd.to_numeric(
    basket["item_count"],
    errors="coerce"
)

seller["total_revenue"] = pd.to_numeric(
    seller["total_revenue"],
    errors="coerce"
)

category_analysis["revenue"] = pd.to_numeric(
    category_analysis["revenue"],
    errors="coerce"
)

regional_analysis["revenue"] = pd.to_numeric(
    regional_analysis["revenue"],
    errors="coerce"
)

rfm["monetary"] = pd.to_numeric(
    rfm["monetary"],
    errors="coerce"
)


# ============================================================
# CORE SALES KPIs
# ============================================================

total_revenue = sales["revenue"].sum()

total_orders = sales["order_id"].nunique()

total_customers = sales[
    "customer_unique_id"
].nunique()

total_items = len(sales)

average_order_value = (
    total_revenue / total_orders
)

average_items_per_order = (
    total_items / total_orders
)


# ============================================================
# CUSTOMER KPIs
# ============================================================

customer_order_counts = (
    sales[
        [
            "customer_unique_id",
            "order_id"
        ]
    ]
    .drop_duplicates()
    .groupby("customer_unique_id")
    ["order_id"]
    .nunique()
)

one_time_customers = (
    customer_order_counts == 1
).sum()

returning_customers = (
    customer_order_counts > 1
).sum()

repeat_customer_rate = (
    returning_customers
    / total_customers
    * 100
)


# ============================================================
# DELIVERY KPIs
# ============================================================

average_delivery_days = (
    delivery["delivery_days"].mean()
)

average_delivery_delay_days = (
    delivery["delivery_delay_days"].mean()
)

total_delivery_orders = len(delivery)

on_time_orders = (
    delivery["delivery_status"]
    .eq("On Time")
    .sum()
)

late_orders = (
    delivery["delivery_status"]
    .eq("Late")
    .sum()
)

on_time_delivery_rate = (
    on_time_orders
    / total_delivery_orders
    * 100
)

late_delivery_rate = (
    late_orders
    / total_delivery_orders
    * 100
)


# ============================================================
# REVIEW KPIs
# ============================================================
#
# review_analysis.csv contains an aggregated score
# distribution, therefore a weighted average is required.
#
# Average Review Score =
# SUM(review_score * review_count) / SUM(review_count)
# ============================================================

total_reviews = reviews["review_count"].sum()

average_review_score = (
    (
        reviews["review_score"]
        * reviews["review_count"]
    ).sum()
    / total_reviews
)

positive_reviews = reviews[
    reviews["review_score"] >= 4
]["review_count"].sum()

negative_reviews = reviews[
    reviews["review_score"] <= 2
]["review_count"].sum()

positive_review_rate = (
    positive_reviews
    / total_reviews
    * 100
)

negative_review_rate = (
    negative_reviews
    / total_reviews
    * 100
)


# ============================================================
# PAYMENT KPIs
# ============================================================

payment_total_row = payments[
    payments["metric"]
    == "total_payment_value"
]

payment_average_row = payments[
    payments["metric"]
    == "average_payment_value"
]

if not payment_total_row.empty:
    total_payment_value = (
        payment_total_row["value"].iloc[0]
    )
else:
    total_payment_value = None

if not payment_average_row.empty:
    average_payment_value = (
        payment_average_row["value"].iloc[0]
    )
else:
    average_payment_value = None


# ============================================================
# BASKET KPIs
# ============================================================

average_basket_value = (
    basket["basket_revenue"].mean()
)

median_basket_value = (
    basket["basket_revenue"].median()
)

average_items_per_basket = (
    basket["item_count"].mean()
)


# ============================================================
# MULTI-ITEM BASKET RATE
# ============================================================

multi_item_orders = (
    basket["item_count"] > 1
).sum()

multi_item_order_rate = (
    multi_item_orders
    / total_orders
    * 100
)


# ============================================================
# SELLER KPIs
# ============================================================

active_sellers = (
    seller["seller_id"].nunique()
)

seller_revenue = (
    seller["total_revenue"].sum()
)

average_revenue_per_seller = (
    seller["total_revenue"].mean()
)


# ============================================================
# SELLER CONCENTRATION
# ============================================================

seller_sorted = seller.sort_values(
    "total_revenue",
    ascending=False
).reset_index(drop=True)

top_10_percent_seller_count = max(
    1,
    int(len(seller_sorted) * 0.10)
)

top_10_percent_seller_revenue = (
    seller_sorted
    .head(top_10_percent_seller_count)
    ["total_revenue"]
    .sum()
)

seller_top_10_revenue_share = (
    top_10_percent_seller_revenue
    / seller_revenue
    * 100
)


# ============================================================
# RFM KPIs
# ============================================================

champions = rfm[
    rfm["segment"] == "Champions"
]

high_value_at_risk = rfm[
    rfm["segment"] == "High Value At Risk"
]

inactive_customers = rfm[
    rfm["segment"] == "Inactive"
]

champion_customers = len(champions)

high_value_at_risk_customers = len(
    high_value_at_risk
)

inactive_customer_count = len(
    inactive_customers
)

champion_revenue = (
    champions["monetary"].sum()
)

high_value_at_risk_revenue = (
    high_value_at_risk["monetary"].sum()
)


# ============================================================
# RFM CUSTOMER PERCENTAGES
# ============================================================

champion_customer_rate = (
    champion_customers
    / total_customers
    * 100
)

high_value_at_risk_rate = (
    high_value_at_risk_customers
    / total_customers
    * 100
)

inactive_customer_rate = (
    inactive_customer_count
    / total_customers
    * 100
)


# ============================================================
# TOP CATEGORY
# ============================================================

top_category = category_analysis.loc[
    category_analysis["revenue"].idxmax()
]

top_category_name = (
    top_category[
        "product_category_name_english"
    ]
)

top_category_revenue = (
    top_category["revenue"]
)


# ============================================================
# TOP STATE
# ============================================================

top_state = regional_analysis.loc[
    regional_analysis["revenue"].idxmax()
]

top_state_name = (
    top_state["customer_state"]
)

top_state_revenue = (
    top_state["revenue"]
)


# ============================================================
# TOP SELLER
# ============================================================

top_seller = seller.loc[
    seller["total_revenue"].idxmax()
]

top_seller_id = (
    top_seller["seller_id"]
)

top_seller_revenue = (
    top_seller["total_revenue"]
)


# ============================================================
# ROUND KPI VALUES
# ============================================================

kpis = [
    ("Total Revenue", total_revenue),
    ("Total Orders", total_orders),
    ("Total Customers", total_customers),
    ("Total Items Sold", total_items),

    ("Average Order Value", average_order_value),
    ("Average Items per Order", average_items_per_order),

    ("Repeat Customer Rate (%)", repeat_customer_rate),

    ("Average Delivery Days", average_delivery_days),
    ("Average Delivery Delay Days", average_delivery_delay_days),
    ("On-Time Delivery Rate (%)", on_time_delivery_rate),
    ("Late Delivery Rate (%)", late_delivery_rate),

    ("Average Review Score", average_review_score),
    ("Positive Review Rate (%)", positive_review_rate),
    ("Negative Review Rate (%)", negative_review_rate),

    ("Total Payment Value", total_payment_value),
    ("Average Payment Value", average_payment_value),

    ("Average Basket Value", average_basket_value),
    ("Median Basket Value", median_basket_value),
    ("Average Items per Basket", average_items_per_basket),
    ("Multi-Item Order Rate (%)", multi_item_order_rate),

    ("Active Sellers", active_sellers),
    ("Average Revenue per Seller", average_revenue_per_seller),
    ("Top 10% Seller Revenue Share (%)", seller_top_10_revenue_share),

    ("Champion Customers", champion_customers),
    ("Champion Customer Rate (%)", champion_customer_rate),
    ("High Value At Risk Customers", high_value_at_risk_customers),
    ("High Value At Risk Rate (%)", high_value_at_risk_rate),
    ("Inactive Customers", inactive_customer_count),
    ("Inactive Customer Rate (%)", inactive_customer_rate),

    ("Champion Revenue", champion_revenue),
    ("High Value At Risk Revenue", high_value_at_risk_revenue),
]


executive_kpis = pd.DataFrame(
    kpis,
    columns=[
        "metric",
        "value"
    ]
)


# ============================================================
# BUSINESS HIGHLIGHTS
# ============================================================

business_highlights = pd.DataFrame(
    [
        {
            "insight": "Top Revenue Category",
            "value": top_category_name,
            "metric_value": top_category_revenue
        },
        {
            "insight": "Top Revenue State",
            "value": top_state_name,
            "metric_value": top_state_revenue
        },
        {
            "insight": "Top Revenue Seller",
            "value": top_seller_id,
            "metric_value": top_seller_revenue
        },
        {
            "insight": "Champion Customers",
            "value": champion_customers,
            "metric_value": champion_revenue
        },
        {
            "insight": "High Value At Risk Customers",
            "value": high_value_at_risk_customers,
            "metric_value": high_value_at_risk_revenue
        },
        {
            "insight": "Inactive Customers",
            "value": inactive_customer_count,
            "metric_value": inactive_customer_count
        },
        {
            "insight": "On-Time Delivery",
            "value": f"{on_time_delivery_rate:.2f}%",
            "metric_value": on_time_delivery_rate
        },
        {
            "insight": "Average Review Score",
            "value": f"{average_review_score:.2f}",
            "metric_value": average_review_score
        }
    ]
)


# ============================================================
# PRINT EXECUTIVE KPIs
# ============================================================

print("\n" + "=" * 70)
print("EXECUTIVE KPI CONSOLIDATION")
print("=" * 70)

print(
    executive_kpis.to_string(
        index=False,
        formatters={
            "value": lambda x: (
                f"{x:,.2f}"
                if isinstance(x, (float, int))
                else str(x)
            )
        }
    )
)


# ============================================================
# PRINT BUSINESS HIGHLIGHTS
# ============================================================

print("\n" + "=" * 70)
print("KEY BUSINESS HIGHLIGHTS")
print("=" * 70)

print(
    business_highlights.to_string(
        index=False
    )
)


# ============================================================
# SAVE OUTPUTS
# ============================================================

executive_kpis.to_csv(
    PROCESSED_DATA / "executive_kpis.csv",
    index=False
)

business_highlights.to_csv(
    PROCESSED_DATA / "business_highlights.csv",
    index=False
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(
    PROCESSED_DATA / "executive_kpis.csv"
)

print(
    PROCESSED_DATA / "business_highlights.csv"
)

print("\n" + "=" * 70)
print("STEP 10 COMPLETED")
print("=" * 70)