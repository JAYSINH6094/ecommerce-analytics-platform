import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


# ============================================================
# LOAD DATA
# ============================================================

reviews = pd.read_csv(
    PROCESSED_DATA / "reviews.csv"
)

sales = pd.read_csv(
    PROCESSED_DATA / "analysis_ready_sales.csv"
)


# ============================================================
# REVIEW SCORE ANALYSIS
# ============================================================

review_summary = (
    reviews["review_score"]
    .value_counts()
    .sort_index()
    .reset_index()
)

review_summary.columns = [
    "review_score",
    "review_count"
]


total_reviews = review_summary["review_count"].sum()

review_summary["percentage"] = (
    review_summary["review_count"]
    / total_reviews
    * 100
).round(2)


# ============================================================
# OVERALL REVIEW METRICS
# ============================================================

average_review_score = reviews["review_score"].mean()

positive_reviews = (
    reviews["review_score"] >= 4
).sum()

negative_reviews = (
    reviews["review_score"] <= 2
).sum()

positive_percentage = (
    positive_reviews / total_reviews * 100
)

negative_percentage = (
    negative_reviews / total_reviews * 100
)


print("\n" + "=" * 70)
print("CUSTOMER REVIEW ANALYSIS")
print("=" * 70)

print(
    f"Total reviews: {total_reviews:,}"
)

print(
    f"Average review score: "
    f"{average_review_score:.2f}"
)

print(
    f"Positive reviews (4-5): "
    f"{positive_reviews:,} "
    f"({positive_percentage:.2f}%)"
)

print(
    f"Negative reviews (1-2): "
    f"{negative_reviews:,} "
    f"({negative_percentage:.2f}%)"
)


print("\n" + "=" * 70)
print("REVIEW SCORE DISTRIBUTION")
print("=" * 70)

print(review_summary.to_string(index=False))


# ============================================================
# REVIEW SCORE BY CATEGORY
# ============================================================

review_category = reviews[
    [
        "order_id",
        "review_score"
    ]
].merge(
    sales[
        [
            "order_id",
            "product_category_name_english"
        ]
    ].drop_duplicates("order_id"),
    on="order_id",
    how="inner"
)


category_reviews = (
    review_category
    .groupby("product_category_name_english")
    .agg(
        average_review_score=("review_score", "mean"),
        review_count=("review_score", "count")
    )
    .reset_index()
)


category_reviews["average_review_score"] = (
    category_reviews["average_review_score"]
    .round(2)
)


category_reviews = category_reviews.sort_values(
    "review_count",
    ascending=False
)


print("\n" + "=" * 70)
print("TOP CATEGORIES BY REVIEW COUNT")
print("=" * 70)

print(
    category_reviews
    .head(10)
    .to_string(index=False)
)


# ============================================================
# REVIEW SCORE BY STATE
# ============================================================

review_state = reviews[
    [
        "order_id",
        "review_score"
    ]
].merge(
    sales[
        [
            "order_id",
            "customer_state"
        ]
    ].drop_duplicates("order_id"),
    on="order_id",
    how="inner"
)


state_reviews = (
    review_state
    .groupby("customer_state")
    .agg(
        average_review_score=("review_score", "mean"),
        review_count=("review_score", "count")
    )
    .reset_index()
)


state_reviews["average_review_score"] = (
    state_reviews["average_review_score"]
    .round(2)
)


state_reviews = state_reviews.sort_values(
    "review_count",
    ascending=False
)


print("\n" + "=" * 70)
print("TOP STATES BY REVIEW COUNT")
print("=" * 70)

print(
    state_reviews
    .head(10)
    .to_string(index=False)
)


# ============================================================
# REVIEW SCORE CHART
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    review_summary["review_score"].astype(str),
    review_summary["review_count"]
)

plt.title("Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")

plt.tight_layout()
plt.show()


# ============================================================
# SAVE RESULTS
# ============================================================

review_output = (
    PROCESSED_DATA /
    "review_analysis.csv"
)

category_review_output = (
    PROCESSED_DATA /
    "category_review_analysis.csv"
)

state_review_output = (
    PROCESSED_DATA /
    "state_review_analysis.csv"
)


review_summary.to_csv(
    review_output,
    index=False
)

category_reviews.to_csv(
    category_review_output,
    index=False
)

state_reviews.to_csv(
    state_review_output,
    index=False
)


print("\n" + "=" * 70)
print("FILES SAVED")
print("=" * 70)

print(review_output)
print(category_review_output)
print(state_review_output)

print("\n" + "=" * 70)
print("STEP 7.7 COMPLETED")
print("=" * 70)