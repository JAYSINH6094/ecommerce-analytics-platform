from pathlib import Path
import json
import urllib.request

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import register_page, html

from dashboard import plotly_theme

from dashboard.components.kpi_card import create_kpi_card
from dashboard.components.chart_card import create_chart_card
from dashboard.components.insight_card import (
    create_insight_card,
    create_insight_item,
)


register_page(
    __name__,
    path="/regional",
    name="Regional",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_csv(filename):

    path = DATA_DIR / filename

    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


regional = load_csv(
    "regional_analysis.csv"
)


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column(df, candidates):

    if df.empty:
        return None

    normalized = {
        str(col)
        .strip()
        .lower()
        .replace(" ", "_"): col
        for col in df.columns
    }

    for candidate in candidates:

        key = (
            candidate
            .lower()
            .replace(" ", "_")
        )

        if key in normalized:
            return normalized[key]

    for col in df.columns:

        col_key = (
            str(col)
            .strip()
            .lower()
            .replace(" ", "_")
        )

        for candidate in candidates:

            candidate_key = (
                candidate
                .lower()
                .replace(" ", "_")
            )

            if (
                candidate_key in col_key
                or col_key in candidate_key
            ):
                return col

    return None


state_col = find_column(
    regional,
    [
        "customer_state",
        "state",
        "customer state",
        "uf",
    ],
)

revenue_col = find_column(
    regional,
    [
        "revenue",
        "total_revenue",
        "sales",
    ],
)

orders_col = find_column(
    regional,
    [
        "orders",
        "total_orders",
        "order_count",
    ],
)

customers_col = find_column(
    regional,
    [
        "customers",
        "unique_customers",
        "customer_count",
    ],
)

aov_col = find_column(
    regional,
    [
        "aov",
        "average_order_value",
        "avg_order_value",
    ],
)

units_col = find_column(
    regional,
    [
        "units_sold",
        "units",
        "quantity",
        "items_sold",
    ],
)


# ============================================================
# NORMALIZE DATA
# ============================================================

if state_col:

    regional[state_col] = (
        regional[state_col]
        .astype(str)
        .str.upper()
        .str.strip()
    )


for column in [
    revenue_col,
    orders_col,
    customers_col,
    aov_col,
    units_col,
]:

    if column:

        regional[column] = pd.to_numeric(
            regional[column],
            errors="coerce",
        )


# ============================================================
# METRIC HELPERS
# ============================================================

def metric_sum(column):

    if (
        column
        and column in regional.columns
    ):
        return regional[column].sum()

    return 0


def metric_mean(column):

    if (
        column
        and column in regional.columns
    ):
        return regional[column].mean()

    return 0


# ============================================================
# KPI VALUES
# ============================================================

total_revenue = metric_sum(
    revenue_col
)

total_orders = metric_sum(
    orders_col
)

total_customers = metric_sum(
    customers_col
)

total_units = metric_sum(
    units_col
)

if total_orders:

    overall_aov = (
        total_revenue
        / total_orders
    )

else:

    overall_aov = 0



# ============================================================
# TOP STATE
# ============================================================

if (
    not regional.empty
    and state_col
    and revenue_col
):

    valid_revenue = regional[
        regional[revenue_col].notna()
    ]

    if not valid_revenue.empty:

        top_row = valid_revenue.loc[
            valid_revenue[
                revenue_col
            ].idxmax()
        ]

        top_state = str(
            top_row[state_col]
        )

        top_state_revenue = float(
            top_row[revenue_col]
        )

    else:

        top_state = "N/A"
        top_state_revenue = 0

else:

    top_state = "N/A"
    top_state_revenue = 0


regional_revenue_share = (
    top_state_revenue
    / total_revenue
    * 100
    if total_revenue
    else 0
)


# ============================================================
# GEOJSON
# ============================================================

GEOJSON_URL = (
    "https://raw.githubusercontent.com/"
    "codeforamerica/"
    "click_that_hood/"
    "master/public/data/"
    "brazil-states.geojson"
)


def load_geojson():

    try:

        with urllib.request.urlopen(
            GEOJSON_URL,
            timeout=5,
        ) as response:

            return json.loads(
                response
                .read()
                .decode("utf-8")
            )

    except Exception:

        return None


def detect_feature_property(
    geojson
):

    if not geojson:
        return None

    features = geojson.get(
        "features",
        [],
    )

    if not features:
        return None

    properties = (
        features[0]
        .get(
            "properties",
            {},
        )
    )

    for candidate in [
        "sigla",
        "UF",
        "uf",
        "abbrev",
        "abbreviation",
        "id",
        "name",
        "nome",
    ]:

        if candidate in properties:
            return candidate

    return None


geojson = load_geojson()

feature_property = (
    detect_feature_property(
        geojson
    )
)


# ============================================================
# BRAZIL REVENUE MAP
# ============================================================

if (
    geojson
    and feature_property
    and state_col
    and revenue_col
    and not regional.empty
):

    map_df = regional[
        [
            state_col,
            revenue_col,
        ]
    ].copy()

    map_df.columns = [
        "state",
        "revenue",
    ]

    map_df["state"] = (
        map_df["state"]
        .astype(str)
        .str.upper()
    )

    fig_map = px.choropleth(
        map_df,
        geojson=geojson,
        locations="state",
        featureidkey=(
            f"properties."
            f"{feature_property}"
        ),
        color="revenue",
        color_continuous_scale=[
            "#101827",
            "#123c52",
            "#176b7b",
            "#22d3ee",
        ],
        hover_name="state",
        hover_data={
            "revenue": ":,.2f",
        },
    )

    fig_map.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="rgba(0,0,0,0)",
    )

    fig_map.update_layout(
        template="analytics_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=0,
            r=0,
            t=8,
            b=0,
        ),
        coloraxis_colorbar=dict(
            title=dict(
                text="Revenue",
                font=dict(
                    color="#91a4b8",
                    size=9,
                ),
            ),
            tickprefix="R$ ",
            thickness=10,
            len=0.65,
            tickfont=dict(
                color="#91a4b8",
                size=9,
            ),
            outlinewidth=0,
        ),
    )

else:

    # ========================================================
    # FALLBACK BAR CHART
    # ========================================================

    if (
        not regional.empty
        and state_col
        and revenue_col
    ):

        fallback = (
            regional
            .nlargest(
                12,
                revenue_col,
            )
            .copy()
        )

    else:

        fallback = pd.DataFrame()

    fig_map = go.Figure()

    if not fallback.empty:

        fig_map.add_trace(
            go.Bar(
                x=fallback[
                    revenue_col
                ],
                y=fallback[
                    state_col
                ],
                orientation="h",
                marker=dict(
                    color="#22d3ee",
                ),
                hovertemplate=(
                    "<b>%{y}</b>"
                    "<br>Revenue: "
                    "R$ %{x:,.2f}"
                    "<extra></extra>"
                ),
            )
        )

    fig_map.update_layout(
        template="analytics_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(
            l=60,
            r=20,
            t=20,
            b=30,
        ),
        showlegend=False,
    )


# ============================================================
# GENERIC STATE BAR CHART
# ============================================================

def make_state_bar(
    column,
    title,
    color="#22d3ee",
    prefix="",
    suffix="",
    decimals=0,
):

    if (
        regional.empty
        or not state_col
        or not column
    ):

        return go.Figure()

    df = regional[
        [
            state_col,
            column,
        ]
    ].dropna(
        subset=[column]
    ).copy()

    df = (
        df
        .nlargest(
            10,
            column,
        )
        .sort_values(
            column,
            ascending=False,
        )
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df[column],
            y=df[state_col],
            orientation="h",
            marker=dict(
                color=color,
            ),
            text=df[column],
            texttemplate=(
                f"{prefix}%{{text:,.{decimals}f}}"
                f"{suffix}"
            ),
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b>"
                f"<br>{title}: "
                f"{prefix}%{{x:,.{decimals}f}}"
                f"{suffix}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        template="analytics_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(
            l=55,
            r=70,
            t=10,
            b=30,
        ),
        showlegend=False,
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=(
            "rgba(148,163,184,0.07)"
        ),
        zeroline=False,
        tickfont=dict(
            color="#708198",
            size=8,
        ),
    )

    fig.update_yaxes(
        autorange="reversed",
        showgrid=False,
        tickfont=dict(
            color="#a9b8c9",
            size=9,
        ),
    )

    return fig


# ============================================================
# CHARTS
# ============================================================

fig_top_revenue = make_state_bar(
    revenue_col,
    "Revenue",
    color="#22d3ee",
    prefix="₹",
    decimals=0,
)

fig_orders = make_state_bar(
    orders_col,
    "Orders",
    color="#8b5cf6",
    decimals=0,
)

fig_customers = make_state_bar(
    customers_col,
    "Customers",
    color="#ec4899",
    decimals=0,
)

fig_aov = make_state_bar(
    aov_col,
    "Average Order Value",
    color="#f59e0b",
    prefix="₹",
    decimals=2,
)


# ============================================================
# REGIONAL INSIGHTS
# ============================================================

if total_revenue:

    top_state_description = (
        f"{top_state} contributes "
        f"₹{top_state_revenue:,.2f}, "
        f"representing "
        f"{regional_revenue_share:.1f}% "
        "of regional revenue."
    )

else:

    top_state_description = (
        "State-level revenue data "
        "is unavailable."
    )


if (
    not regional.empty
    and customers_col
):

    customer_state_row = regional.loc[
        regional[
            customers_col
        ].idxmax()
    ]

    highest_customer_state = str(
        customer_state_row[
            state_col
        ]
    )

    highest_customer_count = int(
        customer_state_row[
            customers_col
        ]
    )

else:

    highest_customer_state = "N/A"
    highest_customer_count = 0


if (
    not regional.empty
    and orders_col
):

    order_state_row = regional.loc[
        regional[
            orders_col
        ].idxmax()
    ]

    highest_order_state = str(
        order_state_row[
            state_col
        ]
    )

    highest_order_count = int(
        order_state_row[
            orders_col
        ]
    )

else:

    highest_order_state = "N/A"
    highest_order_count = 0


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
                            "REGIONAL",
                            className="page-eyebrow",
                        ),

                        html.H1(
                            "Regional Performance",
                            className="page-title",
                        ),

                        html.P(
                            (
                                "Revenue, customer, "
                                "order and basket-value "
                                "performance across "
                                "Brazilian states."
                            ),
                            className="page-subtitle",
                        ),

                    ],
                    className="regional-heading",
                ),

                create_insight_card(
                    label="Key Insight",
                    title=(
                        f"{top_state} generated "
                        f"₹{top_state_revenue / 1_000_000:.2f}M "
                        "in revenue."
                    ),
                    description=(
                        f"{top_state_description}"
                    ),
                    icon="✦",
                    variant="cyan",
                ),

            ],
            className="regional-header",
        ),


        # ====================================================
        # KPI GRID
        # ====================================================

        html.Div(
            [

                create_kpi_card(
                    title="Regional Revenue",
                    value=(
                        f"₹"
                        f"{total_revenue / 1_000_000:.2f}M"
                    ),
                    icon="↗",
                    variant="cyan",
                    subtitle="Revenue across states",
                ),

                create_kpi_card(
                    title="Orders",
                    value=f"{total_orders:,.0f}",
                    icon="▤",
                    variant="violet",
                    subtitle="Regional order records",
                ),

                create_kpi_card(
                    title="Customers",
                    value=f"{total_customers:,.0f}",
                    icon="◎",
                    variant="pink",
                    subtitle="State-level unique customer counts",
                ),

                create_kpi_card(
                    title="Average Order Value",
                    value=f"₹{overall_aov:,.2f}",
                    icon="◈",
                    variant="amber",
                    subtitle="Average regional basket",
                ),

                create_kpi_card(
                    title="Units Sold",
                    value=f"{total_units:,.0f}",
                    icon="▥",
                    variant="cyan",
                    subtitle="Units across regions",
                ),

            ],
            className="kpi-grid regional-kpi-grid",
        ),


        # ====================================================
        # MAP + TOP STATES
        # ====================================================

        html.Div(
            [

                create_chart_card(
                    title="Revenue by State",
                    subtitle="Revenue concentration across Brazil",
                    figure=fig_map,
                    class_name="regional-map-card",
                    height=390,
                ),

                create_chart_card(
                    title="Top States by Revenue",
                    subtitle="Highest-revenue geographic markets",
                    figure=fig_top_revenue,
                    class_name="regional-top-state-card",
                    height=390,
                ),

            ],
            className="regional-main-grid",
        ),


        # ====================================================
        # SECONDARY ANALYTICS
        # ====================================================

        html.Div(
            [

                create_chart_card(
                    title="Orders by State",
                    subtitle="Regional order volume",
                    figure=fig_orders,
                    class_name="regional-orders-card",
                    height=300,
                ),

                create_chart_card(
                    title="Customers by State",
                    subtitle="Regional customer concentration",
                    figure=fig_customers,
                    class_name="regional-customers-card",
                    height=300,
                ),

                create_chart_card(
                    title="Average Order Value",
                    subtitle="Regional basket value",
                    figure=fig_aov,
                    class_name="regional-aov-card",
                    height=300,
                ),

            ],
            className="regional-secondary-grid",
        ),


        # ====================================================
        # BUSINESS INSIGHTS
        # ====================================================

        html.Div(
            [

                create_insight_item(
                    title="Revenue leader",
                    description=(
                        f"{top_state} contributes "
                        f"₹{top_state_revenue:,.0f} "
                        f"or {regional_revenue_share:.1f}% "
                        "of regional revenue."
                    ),
                    icon="◆",
                    variant="cyan",
                ),

                create_insight_item(
                    title="Customer concentration",
                    description=(
                        f"{highest_customer_state} has "
                        f"{highest_customer_count:,} "
                        "customers in the regional analysis."
                    ),
                    icon="◎",
                    variant="pink",
                ),

                create_insight_item(
                    title="Order concentration",
                    description=(
                        f"{highest_order_state} records "
                        f"{highest_order_count:,} "
                        "orders."
                    ),
                    icon="▤",
                    variant="violet",
                ),

            ],
            className="regional-insights-grid",
        ),


        # ====================================================
        # FOOTNOTE
        # ====================================================

        html.Div(
            [
                html.Span(
                    "Source: Olist Brazilian E-Commerce Public Dataset"
                ),
                html.Span(
                    "Regional analytics: Validated"
                ),
            ],
            className="page-footnote",
        ),

    ],
    className="regional-page",
)