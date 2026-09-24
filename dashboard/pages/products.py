import os

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html

from dashboard import plotly_theme
from dashboard.components.kpi_card import create_kpi_card
from dashboard.components.chart_card import create_chart_card
from dashboard.components.insight_card import (
    create_insight_card,
    create_insight_item,
)


dash.register_page(__name__, path="/products")


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

PROCESSED_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
)

CATEGORY_FILE = os.path.join(
    PROCESSED_DIR,
    "category_analysis.csv",
)

PRODUCT_FILE = os.path.join(
    PROCESSED_DIR,
    "product_analysis.csv",
)


# ============================================================
# LOAD DATA
# ============================================================

category_analysis = pd.read_csv(
    CATEGORY_FILE
)

product_analysis = pd.read_csv(
    PRODUCT_FILE
)


# ============================================================
# NORMALIZE COLUMN NAMES
# ============================================================

category_analysis.columns = [
    column.strip()
    for column in category_analysis.columns
]

product_analysis.columns = [
    column.strip()
    for column in product_analysis.columns
]


# ============================================================
# HELPERS
# ============================================================

def find_column(df, candidates):

    for candidate in candidates:

        if candidate in df.columns:
            return candidate

    return None


def format_number(value):
    return f"{value:,.0f}"


def format_currency(value):
    return f"R${value:,.2f}"


def format_millions(value):
    return f"R${value / 1_000_000:.2f}M"


def clean_category_name(value):
    value = str(value)

    if value.lower() in {
        "nan",
        "none",
        "",
    }:
        return "Unknown"

    return value.replace("_", " ").title()


# ============================================================
# IDENTIFY COLUMNS
# ============================================================

category_col = find_column(
    category_analysis,
    [
        "product_category_name_english",
        "product_category_name",
        "category",
    ],
)

category_revenue_col = find_column(
    category_analysis,
    [
        "revenue",
        "total_revenue",
        "category_revenue",
    ],
)

category_units_col = find_column(
    category_analysis,
    [
        "units_sold",
        "quantity",
        "total_units",
        "items_sold",
    ],
)

product_id_col = find_column(
    product_analysis,
    [
        "product_id",
        "product",
    ],
)

product_revenue_col = find_column(
    product_analysis,
    [
        "revenue",
        "total_revenue",
        "product_revenue",
    ],
)

product_units_col = find_column(
    product_analysis,
    [
        "units_sold",
        "quantity",
        "total_units",
        "items_sold",
    ],
)

product_price_col = find_column(
    product_analysis,
    [
        "average_price",
        "avg_price",
        "price",
    ],
)

product_category_col = find_column(
    product_analysis,
    [
        "product_category_name_english",
        "product_category_name",
        "category",
    ],
)


# ============================================================
# DATA CLEANING
# ============================================================

if category_revenue_col:
    category_analysis[
        category_revenue_col
    ] = pd.to_numeric(
        category_analysis[
            category_revenue_col
        ],
        errors="coerce",
    ).fillna(0)

if category_units_col:
    category_analysis[
        category_units_col
    ] = pd.to_numeric(
        category_analysis[
            category_units_col
        ],
        errors="coerce",
    ).fillna(0)

if product_revenue_col:
    product_analysis[
        product_revenue_col
    ] = pd.to_numeric(
        product_analysis[
            product_revenue_col
        ],
        errors="coerce",
    ).fillna(0)

if product_units_col:
    product_analysis[
        product_units_col
    ] = pd.to_numeric(
        product_analysis[
            product_units_col
        ],
        errors="coerce",
    ).fillna(0)

if product_price_col:
    product_analysis[
        product_price_col
    ] = pd.to_numeric(
        product_analysis[
            product_price_col
        ],
        errors="coerce",
    )


# ============================================================
# PRODUCT KPIs
# ============================================================

total_products = len(product_analysis)

total_categories = len(
    category_analysis
)

total_units = (
    int(
        product_analysis[
            product_units_col
        ].sum()
    )
    if product_units_col
    else 0
)

total_revenue = (
    float(
        category_analysis[
            category_revenue_col
        ].sum()
    )
    if category_revenue_col
    else 0
)

average_price = (
    float(
        product_analysis[
            product_price_col
        ].mean()
    )
    if product_price_col
    else 0
)


# ============================================================
# KPI MICRO-VISUAL REFERENCES
# ============================================================

if (
    product_category_col
    and total_products
    and not product_analysis.empty
):
    product_category_counts = (
        product_analysis[product_category_col]
        .fillna("Unknown")
        .value_counts()
    )
    largest_category_product_share = (
        product_category_counts.iloc[0]
        / total_products
        * 100
        if not product_category_counts.empty
        else 0
    )
else:
    largest_category_product_share = 0

if category_revenue_col and total_revenue:
    top_three_category_revenue_share = (
        category_analysis
        .sort_values(
            category_revenue_col,
            ascending=False,
        )
        .head(3)[category_revenue_col]
        .sum()
        / total_revenue
        * 100
    )
else:
    top_three_category_revenue_share = 0

if category_units_col and not category_analysis.empty:
    total_category_units = category_analysis[
        category_units_col
    ].sum()
    top_category_volume_share = (
        category_analysis[
            category_units_col
        ].max()
        / total_category_units
        * 100
        if total_category_units
        else 0
    )
else:
    top_category_volume_share = 0

if product_price_col and not product_analysis.empty:
    average_price_percentile = (
        product_analysis[
            product_price_col
        ]
        .le(average_price)
        .mean()
        * 100
    )
else:
    average_price_percentile = 0


# ============================================================
# TOP CATEGORY
# ============================================================

if (
    category_col
    and category_revenue_col
    and not category_analysis.empty
):

    top_category_row = (
        category_analysis
        .sort_values(
            category_revenue_col,
            ascending=False,
        )
        .iloc[0]
    )

    top_category = clean_category_name(
        top_category_row[category_col]
    )

    top_category_revenue = float(
        top_category_row[
            category_revenue_col
        ]
    )

else:

    top_category = "Unavailable"
    top_category_revenue = 0


category_share = (
    top_category_revenue
    / total_revenue
    * 100
    if total_revenue
    else 0
)


# ============================================================
# TREEMAP
# ============================================================

if (
    category_col
    and category_revenue_col
):

    treemap_data = (
        category_analysis[
            [
                category_col,
                category_revenue_col,
            ]
        ]
        .copy()
    )

    treemap_data = treemap_data[
        treemap_data[
            category_revenue_col
        ] > 0
    ]

    treemap_data["display_category"] = (
        treemap_data[
            category_col
        ].apply(clean_category_name)
    )

else:

    treemap_data = pd.DataFrame(
        columns=[
            "display_category",
            "revenue",
        ]
    )


fig_treemap = px.treemap(
    treemap_data,
    path=["display_category"],
    values=category_revenue_col,
    color=category_revenue_col,
    color_continuous_scale=[
        "#111827",
        "#173c4a",
        "#17656f",
        "#1aa5a8",
        "#22d3ee",
    ],
)

fig_treemap.update_traces(
    textinfo="label+value",
    texttemplate=(
        "<b>%{label}</b>"
        "<br>R$%{value:,.0f}"
    ),
    textfont=dict(
        size=10,
        color="#ecfeff",
    ),
    hovertemplate=(
        "<b>%{label}</b>"
        "<br>Revenue: R$%{value:,.2f}"
        "<extra></extra>"
    ),
    marker=dict(
        line=dict(
            color="#0a101b",
            width=2,
        )
    ),
)

fig_treemap.update_layout(
    template="analytics_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=340,
    margin=dict(
        l=5,
        r=5,
        t=5,
        b=5,
    ),
    coloraxis_showscale=False,
)


# ============================================================
# TOP PRODUCTS
# ============================================================

if (
    product_id_col
    and product_revenue_col
):

    top_products = (
        product_analysis
        .sort_values(
            product_revenue_col,
            ascending=False,
        )
        .head(8)
        .copy()
    )

else:

    top_products = pd.DataFrame()


def short_product_id(value):

    value = str(value)

    if len(value) <= 10:
        return value

    return value[:8] + "..."


if not top_products.empty:

    top_products["short_id"] = (
        top_products[
            product_id_col
        ].apply(short_product_id)
    )

    if product_category_col:

        top_products["display_name"] = (
            top_products[
                product_category_col
            ]
            .fillna("Unknown")
            .apply(clean_category_name)
            + " · "
            + top_products["short_id"]
        )

    else:

        top_products["display_name"] = (
            top_products["short_id"]
        )


fig_products = go.Figure()

if not top_products.empty:

    top_products = (
        top_products
        .sort_values(
            product_revenue_col,
            ascending=True,
        )
    )

    fig_products.add_trace(
        go.Bar(
            x=top_products[
                product_revenue_col
            ],
            y=top_products[
                "display_name"
            ],
            orientation="h",
            marker=dict(
                color=[
                    "#8b5cf6",
                    "#8b5cf6",
                    "#8b5cf6",
                    "#8b5cf6",
                    "#7c6ee6",
                    "#6f82d7",
                    "#5f9dd1",
                    "#22d3ee",
                ][:len(top_products)]
            ),
            text=top_products[
                product_revenue_col
            ],
            texttemplate="R$%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            customdata=top_products[
                [product_id_col]
            ],
            hovertemplate=(
                "<b>%{y}</b>"
                "<br>Product ID: %{customdata[0]}"
                "<br>Revenue: R$%{x:,.2f}"
                "<extra></extra>"
            ),
        )
    )

fig_products.update_layout(
    template="analytics_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=340,
    margin=dict(
        l=145,
        r=85,
        t=5,
        b=25,
    ),
    showlegend=False,
)

fig_products.update_xaxes(
    showgrid=True,
    gridcolor="rgba(148,163,184,0.07)",
    zeroline=False,
    tickfont=dict(
        color="#708198",
        size=8,
    ),
)

fig_products.update_yaxes(
    showgrid=False,
    tickfont=dict(
        color="#a9b8c9",
        size=8,
    ),
)


# ============================================================
# UNITS SOLD BY CATEGORY
# ============================================================

fig_units = go.Figure()

if (
    category_col
    and category_units_col
):

    units_data = (
        category_analysis
        .sort_values(
            category_units_col,
            ascending=False,
        )
        .head(8)
        .copy()
    )

    units_data["display_category"] = (
        units_data[
            category_col
        ].apply(clean_category_name)
    )

    units_data = (
        units_data
        .sort_values(
            category_units_col,
            ascending=True,
        )
    )

    fig_units.add_trace(
        go.Bar(
            x=units_data[
                category_units_col
            ],
            y=units_data[
                "display_category"
            ],
            orientation="h",
            marker=dict(
                color="#22d3ee"
            ),
            text=units_data[
                category_units_col
            ],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b>"
                "<br>Units Sold: %{x:,}"
                "<extra></extra>"
            ),
        )
    )

else:

    fig_units.add_annotation(
        text="Units data unavailable",
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            color="#708198",
            size=10,
        ),
    )

fig_units.update_layout(
    template="analytics_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=300,
    margin=dict(
        l=145,
        r=75,
        t=5,
        b=25,
    ),
    showlegend=False,
)

fig_units.update_xaxes(
    showgrid=True,
    gridcolor="rgba(148,163,184,0.07)",
    zeroline=False,
    tickfont=dict(
        color="#708198",
        size=8,
    ),
)

fig_units.update_yaxes(
    showgrid=False,
    tickfont=dict(
        color="#a9b8c9",
        size=8,
    ),
)


# ============================================================
# AVERAGE PRICE BY CATEGORY
# ============================================================

fig_price = go.Figure()

if (
    product_price_col
    and product_category_col
):

    price_data = (
        product_analysis
        .dropna(
            subset=[
                product_category_col,
                product_price_col,
            ]
        )
        .groupby(
            product_category_col,
            as_index=False,
        )[product_price_col]
        .mean()
        .sort_values(
            product_price_col,
            ascending=False,
        )
        .head(8)
    )

    price_data["display_category"] = (
        price_data[
            product_category_col
        ].apply(clean_category_name)
    )

    price_data = (
        price_data
        .sort_values(
            product_price_col,
            ascending=True,
        )
    )

    fig_price.add_trace(
        go.Bar(
            x=price_data[
                product_price_col
            ],
            y=price_data[
                "display_category"
            ],
            orientation="h",
            marker=dict(
                color="#f59e0b"
            ),
            text=price_data[
                product_price_col
            ],
            texttemplate="R$%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b>"
                "<br>Average Price: R$%{x:,.2f}"
                "<extra></extra>"
            ),
        )
    )

else:

    fig_price.add_annotation(
        text="Pricing data unavailable",
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            color="#708198",
            size=10,
        ),
    )

fig_price.update_layout(
    template="analytics_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=300,
    margin=dict(
        l=145,
        r=75,
        t=5,
        b=25,
    ),
    showlegend=False,
)

fig_price.update_xaxes(
    showgrid=True,
    gridcolor="rgba(148,163,184,0.07)",
    zeroline=False,
    tickfont=dict(
        color="#708198",
        size=8,
    ),
)

fig_price.update_yaxes(
    showgrid=False,
    tickfont=dict(
        color="#a9b8c9",
        size=8,
    ),
)


# ============================================================
# PRODUCT INSIGHTS
# ============================================================

top_categories = (
    category_analysis
    .sort_values(
        category_revenue_col,
        ascending=False,
    )
    .head(3)
    .copy()
)

if category_units_col:
    highest_volume_category = (
        category_analysis
        .sort_values(
            category_units_col,
            ascending=False,
        )
        .iloc[0]
    )

    highest_volume_name = clean_category_name(
        highest_volume_category[
            category_col
        ]
    )

    highest_volume_units = int(
        highest_volume_category[
            category_units_col
        ]
    )
else:
    highest_volume_name = "Unavailable"
    highest_volume_units = 0


# ============================================================
# PAGE
# ============================================================

layout = html.Div(
    [

        # ====================================================
        # HEADER
        # ====================================================

        html.Div(
            [

                html.Div(
                    [

                        html.Div(
                            "PRODUCTS",
                            className="page-eyebrow",
                        ),

                        html.H1(
                            "Product Intelligence",
                            className="page-title",
                        ),

                        html.P(
                            (
                                "Category performance, "
                                "product concentration, "
                                "sales volume and pricing "
                                "from the historical dataset."
                            ),
                            className="page-description",
                        ),

                    ],
                    className="products-heading",
                ),

                create_insight_card(
                    label="Key Insight",
                    title=(
                        f"{top_category} generated "
                        f"{format_millions(top_category_revenue)} "
                        f"and represented "
                        f"{category_share:.1f}% of category revenue."
                    ),
                    description=(
                        f"The highest-volume category is "
                        f"{highest_volume_name}, with "
                        f"{format_number(highest_volume_units)} "
                        "units sold."
                    ),
                    icon="✦",
                    variant="cyan",
                ),

            ],
            className="products-header",
        ),


        # ====================================================
        # KPI GRID
        # ====================================================

        html.Div(
            [

                create_kpi_card(
                    title="Total Products",
                    value=format_number(total_products),
                    icon="◇",
                    variant="cyan",
                    subtitle="Products in analysis",
                    sparkline=html.Div(
                        [
                            html.Span(
                                className="kpi-meter-fill",
                                style={
                                    "width": (
                                        f"{largest_category_product_share:.1f}%"
                                    ),
                                },
                            ),
                            html.Span(
                                f"Largest category {largest_category_product_share:.1f}%",
                                className="kpi-meter-label",
                            ),
                        ],
                        className="kpi-meter kpi-meter-cyan",
                    ),
                ),

                create_kpi_card(
                    title="Categories",
                    value=format_number(total_categories),
                    icon="◈",
                    variant="violet",
                    subtitle="Product categories",
                    sparkline=html.Div(
                        [
                            html.Span(
                                className="kpi-meter-fill",
                                style={
                                    "width": (
                                        f"{top_three_category_revenue_share:.1f}%"
                                    ),
                                },
                            ),
                            html.Span(
                                f"Top 3 revenue {top_three_category_revenue_share:.1f}%",
                                className="kpi-meter-label",
                            ),
                        ],
                        className="kpi-meter kpi-meter-violet",
                    ),
                ),

                create_kpi_card(
                    title="Units Sold",
                    value=format_number(total_units),
                    icon="▥",
                    variant="pink",
                    subtitle="Total units sold",
                    sparkline=html.Div(
                        [
                            html.Span(
                                className="kpi-meter-fill",
                                style={
                                    "width": (
                                        f"{top_category_volume_share:.1f}%"
                                    ),
                                },
                            ),
                            html.Span(
                                f"Top category {top_category_volume_share:.1f}%",
                                className="kpi-meter-label",
                            ),
                        ],
                        className="kpi-meter kpi-meter-pink",
                    ),
                ),

                create_kpi_card(
                    title="Average Price",
                    value=format_currency(average_price),
                    icon="R$",
                    variant="amber",
                    subtitle="Average product price",
                    sparkline=html.Div(
                        [
                            html.Span(
                                className="kpi-meter-fill",
                                style={
                                    "width": (
                                        f"{average_price_percentile:.1f}%"
                                    ),
                                },
                            ),
                            html.Span(
                                f"Price percentile {average_price_percentile:.0f}"
                                + (
                                    "th"
                                    if 10 <= int(average_price_percentile) % 100 <= 20
                                    else {
                                        1: "st",
                                        2: "nd",
                                        3: "rd",
                                    }.get(int(average_price_percentile) % 10, "th")
                                ),
                                className="kpi-meter-label",
                            ),
                        ],
                        className="kpi-meter kpi-meter-amber",
                    ),
                ),

                create_kpi_card(
                    title="Category Revenue",
                    value=format_millions(total_revenue),
                    icon="◆",
                    variant="cyan",
                    subtitle="Revenue across categories",
                    sparkline=html.Div(
                        [
                            html.Span(
                                className="kpi-meter-fill",
                                style={
                                    "width": f"{category_share:.1f}%",
                                },
                            ),
                            html.Span(
                                f"Top category {category_share:.1f}%",
                                className="kpi-meter-label",
                            ),
                        ],
                        className="kpi-meter kpi-meter-cyan-alt",
                    ),
                ),

            ],
            className="kpi-grid products-kpi-grid",
        ),


        # ====================================================
        # MAIN PRODUCT BENTO
        # ====================================================

        html.Div(
            [

                create_chart_card(
                    title="Revenue by Product Category",
                    subtitle="Category revenue contribution",
                    figure=fig_treemap,
                    class_name="products-treemap-card",
                    height=340,
                ),

                create_chart_card(
                    title="Top Products by Revenue",
                    subtitle="Highest-revenue products",
                    figure=fig_products,
                    class_name="products-top-products-card",
                    height=340,
                ),

            ],
            className="products-main-grid",
        ),


        # ====================================================
        # SECONDARY ANALYTICS
        # ====================================================

        html.Div(
            [

                create_chart_card(
                    title="Units Sold by Category",
                    subtitle="Highest-volume categories",
                    figure=fig_units,
                    class_name="products-units-card",
                    height=300,
                ),

                create_chart_card(
                    title="Average Product Price",
                    subtitle="Average price by category",
                    figure=fig_price,
                    class_name="products-price-card",
                    height=300,
                ),

            ],
            className="products-secondary-grid",
        ),


        # ====================================================
        # BUSINESS INSIGHTS
        # ====================================================

        html.Div(
            [

                create_insight_item(
                    title="Category concentration",
                    description=(
                        f"{top_category} contributes "
                        f"{category_share:.1f}% of category revenue."
                    ),
                    icon="◆",
                    variant="cyan",
                ),

                create_insight_item(
                    title="Highest-volume category",
                    description=(
                        f"{highest_volume_name} leads volume "
                        f"with {format_number(highest_volume_units)} "
                        "units sold."
                    ),
                    icon="▥",
                    variant="violet",
                ),

                create_insight_item(
                    title="Product catalog",
                    description=(
                        f"The analysis covers "
                        f"{format_number(total_products)} products "
                        f"across {format_number(total_categories)} "
                        "categories."
                    ),
                    icon="◇",
                    variant="pink",
                ),

            ],
            className="products-insights-grid",
        ),


        html.Div(
            [
                html.Span(
                    "Source: Olist Brazilian E-Commerce Public Dataset"
                ),
                html.Span(
                    "Product analytics: Validated"
                ),
            ],
            className="page-footnote",
        ),

    ],
    className="products-page",
)
