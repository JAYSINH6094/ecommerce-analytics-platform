import os

import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

from dashboard import plotly_theme
from dashboard.components.kpi_card import create_kpi_card
from dashboard.components.chart_card import create_chart_card
from dashboard.components.insight_card import (
    create_insight_card,
    create_insight_item,
)

dash.register_page(__name__, path="/")


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

PROCESSED_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
)


KPI_FILE = os.path.join(
    PROCESSED_DIR,
    "executive_kpis.csv",
)

MONTHLY_FILE = os.path.join(
    PROCESSED_DIR,
    "monthly_sales_analysis.csv",
)

CATEGORY_FILE = os.path.join(
    PROCESSED_DIR,
    "category_analysis.csv",
)

ORDERS_FILE = os.path.join(
    PROCESSED_DIR,
    "orders.csv",
)

REGIONAL_FILE = os.path.join(
    PROCESSED_DIR,
    "regional_analysis.csv",
)


# ============================================================
# LOAD DATA
# ============================================================

def load_kpis():
    df = pd.read_csv(KPI_FILE)
    return dict(zip(df["metric"], df["value"]))


kpis = load_kpis()

monthly_sales = pd.read_csv(MONTHLY_FILE)
category_analysis = pd.read_csv(CATEGORY_FILE)
orders = pd.read_csv(ORDERS_FILE)
regional_analysis = pd.read_csv(REGIONAL_FILE)


# ============================================================
# DATA PREPARATION
# ============================================================

monthly_sales["order_month"] = pd.to_datetime(
    monthly_sales["order_month"],
    errors="coerce",
)

monthly_sales = (
    monthly_sales
    .dropna(subset=["order_month"])
    .sort_values("order_month")
    .reset_index(drop=True)
)


orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce",
)

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"],
    errors="coerce",
)

orders["order_estimated_delivery_date"] = pd.to_datetime(
    orders["order_estimated_delivery_date"],
    errors="coerce",
)


# ============================================================
# KPI VALUES
# ============================================================

revenue = float(kpis["Total Revenue"])
orders_count = int(float(kpis["Total Orders"]))
customers = int(float(kpis["Total Customers"]))
aov = float(kpis["Average Order Value"])
repeat_rate = float(kpis["Repeat Customer Rate (%)"])


# ============================================================
# ON-TIME DELIVERY
# ============================================================

delivered = orders[
    orders["order_status"].eq("delivered")
].copy()

delivery_comparable = delivered[
    delivered["order_delivered_customer_date"].notna()
    & delivered["order_estimated_delivery_date"].notna()
].copy()

if not delivery_comparable.empty:

    on_time_rate = (
        (
            delivery_comparable[
                "order_delivered_customer_date"
            ]
            <=
            delivery_comparable[
                "order_estimated_delivery_date"
            ]
        ).mean()
        * 100
    )

else:
    on_time_rate = 0.0


# ============================================================
# FORMATTING
# ============================================================

def format_currency(value):
    return f"₹{value:,.2f}"


def format_millions(value):
    return f"₹{value / 1_000_000:.2f}M"


def format_number(value):
    return f"{value:,.0f}"


def format_percent(value):
    return f"{value:.2f}%"


def clean_category_name(value):
    return (
        str(value)
        .replace("_", " ")
        .title()
    )


# ============================================================
# REVENUE MOM
# ============================================================

if len(monthly_sales) >= 2:

    latest_revenue = float(
        monthly_sales.iloc[-1]["revenue"]
    )

    previous_revenue = float(
        monthly_sales.iloc[-2]["revenue"]
    )

    if previous_revenue != 0:

        revenue_mom = (
            (latest_revenue - previous_revenue)
            / previous_revenue
        ) * 100

    else:
        revenue_mom = 0.0

else:
    revenue_mom = 0.0


# ============================================================
# TOP CATEGORY
# ============================================================

category_analysis = (
    category_analysis
    .dropna(
        subset=[
            "product_category_name_english",
            "revenue",
        ]
    )
    .copy()
)

category_analysis["category_display"] = (
    category_analysis[
        "product_category_name_english"
    ].map(clean_category_name)
)

top_category_row = (
    category_analysis
    .sort_values(
        "revenue",
        ascending=False,
    )
    .iloc[0]
)

top_category = top_category_row[
    "category_display"
]

top_category_revenue = float(
    top_category_row["revenue"]
)

category_total = float(
    category_analysis["revenue"].sum()
)

top_category_share = (
    top_category_revenue
    / category_total
    * 100
    if category_total
    else 0
)


# ============================================================
# PEAK MONTH
# ============================================================

peak_row = monthly_sales.loc[
    monthly_sales["revenue"].idxmax()
]

peak_month = pd.to_datetime(
    peak_row["order_month"]
).strftime("%b %Y")

peak_revenue = float(
    peak_row["revenue"]
)


# ============================================================
# CUSTOMER GROWTH
# ============================================================

if "customer_id" in orders.columns:

    customer_growth = (
        orders
        .dropna(
            subset=[
                "order_purchase_timestamp",
                "customer_id",
            ]
        )
        .assign(
            order_month=lambda df:
            df["order_purchase_timestamp"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )
        .groupby("order_month")["customer_id"]
        .nunique()
        .reset_index(
            name="customers"
        )
        .sort_values("order_month")
    )

else:

    customer_growth = pd.DataFrame(
        columns=[
            "order_month",
            "customers",
        ]
    )


# ============================================================
# COLORS
# ============================================================

CYAN = "#22d3ee"
VIOLET = "#8b5cf6"
PINK = "#ec4899"
AMBER = "#f59e0b"
GREEN = "#34d399"
BLUE = "#60a5fa"

TEXT = "#dbe7f1"
MUTED = "#708198"
GRID = "rgba(148,163,184,0.075)"


STATUS_COLORS = {
    "delivered": CYAN,
    "shipped": VIOLET,
    "canceled": PINK,
    "unavailable": GREEN,
    "invoiced": AMBER,
    "processing": BLUE,
    "created": "#a78bfa",
    "approved": "#64748b",
}


# ============================================================
# COMMON CHART CONFIG
# ============================================================

def apply_chart_layout(
    figure,
    height=330,
    margin=None,
):

    if margin is None:
        margin = dict(
            l=42,
            r=18,
            t=10,
            b=38,
        )

    figure.update_layout(
        template="analytics_dark",
        height=height,
        margin=margin,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color=TEXT,
            size=9,
        ),
        hoverlabel=dict(
            bgcolor="#0b1422",
            bordercolor="rgba(103,232,249,0.25)",
            font=dict(
                color="#eef7fb",
                size=10,
            ),
        ),
    )

    figure.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        showline=False,
        tickfont=dict(
            color=MUTED,
            size=8,
        ),
        title=None,
    )

    figure.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        showline=False,
        tickfont=dict(
            color=MUTED,
            size=8,
        ),
        title=None,
    )

    return figure


# ============================================================
# REVENUE TREND
# ============================================================

fig_revenue = go.Figure()

fig_revenue.add_trace(
    go.Scatter(
        x=monthly_sales["order_month"],
        y=monthly_sales["revenue"],
        mode="lines",
        name="Revenue",
        line=dict(
            color=CYAN,
            width=3,
            shape="spline",
        ),
        fill="tozeroy",
        fillcolor="rgba(34,211,238,0.06)",
        hovertemplate=(
            "<b>%{x|%b %Y}</b>"
            "<br>Revenue: ₹%{y:,.2f}"
            "<extra></extra>"
        ),
    )
)

fig_revenue.add_trace(
    go.Scatter(
        x=[peak_row["order_month"]],
        y=[peak_revenue],
        mode="markers",
        name="Peak",
        marker=dict(
            size=10,
            color=PINK,
            line=dict(
                color="#fbcfe8",
                width=2,
            ),
        ),
        hovertemplate=(
            "<b>Peak Month</b>"
            "<br>%{x|%b %Y}"
            "<br>₹%{y:,.2f}"
            "<extra></extra>"
        ),
    )
)

fig_revenue.update_layout(
    hovermode="x unified",
    showlegend=False,
)

apply_chart_layout(
    fig_revenue,
    height=330,
    margin=dict(
        l=48,
        r=18,
        t=8,
        b=38,
    ),
)


# ============================================================
# ORDER STATUS
# ============================================================

order_status = (
    orders["order_status"]
    .dropna()
    .value_counts()
    .reset_index()
)

order_status.columns = [
    "order_status",
    "order_count",
]

fig_status = go.Figure()

fig_status.add_trace(
    go.Pie(
        labels=order_status["order_status"],
        values=order_status["order_count"],
        hole=0.68,
        sort=False,
        marker=dict(
            colors=[
                STATUS_COLORS.get(
                    str(status),
                    "#64748b",
                )
                for status in order_status["order_status"]
            ],
            line=dict(
                color="#09111d",
                width=2,
            ),
        ),
        textinfo="none",
        hovertemplate=(
            "<b>%{label}</b>"
            "<br>Orders: %{value:,}"
            "<br>Share: %{percent}"
            "<extra></extra>"
        ),
    )
)

fig_status.add_annotation(
    text=(
        f"<b>{format_number(orders_count)}</b>"
        "<br><span style='font-size:9px'>Orders</span>"
    ),
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(
        color="#edf6fb",
        size=16,
    ),
)

fig_status.update_layout(
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.01,
        font=dict(
            color="#aab8c8",
            size=8,
        ),
    ),
)

apply_chart_layout(
    fig_status,
    height=330,
    margin=dict(
        l=8,
        r=90,
        t=5,
        b=5,
    ),
)


# ============================================================
# TOP 5 CATEGORIES
# ============================================================

top_categories = (
    category_analysis
    .sort_values(
        "revenue",
        ascending=False,
    )
    .head(5)
    .sort_values(
        "revenue",
        ascending=True,
    )
)

fig_categories = go.Figure()

fig_categories.add_trace(
    go.Bar(
        x=top_categories["revenue"],
        y=top_categories["category_display"],
        orientation="h",
        marker=dict(
            color=[
                "#6475d4",
                "#8177db",
                "#8b5cf6",
                "#9b62ed",
                CYAN,
            ]
        ),
        text=[
            f"₹{value:,.0f}"
            for value in top_categories["revenue"]
        ],
        textposition="outside",
        textfont=dict(
            color="#b8c7d6",
            size=8,
        ),
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>Revenue: ₹%{x:,.2f}"
            "<extra></extra>"
        ),
    )
)

fig_categories.update_layout(
    showlegend=False,
)

fig_categories.update_xaxes(
    tickformat=".2s",
)

apply_chart_layout(
    fig_categories,
    height=300,
    margin=dict(
        l=120,
        r=62,
        t=5,
        b=30,
    ),
)


# ============================================================
# REVENUE BY STATE
# ============================================================

top_states = (
    regional_analysis
    .dropna(
        subset=[
            "customer_state",
            "revenue",
        ]
    )
    .sort_values(
        "revenue",
        ascending=False,
    )
    .head(7)
    .sort_values(
        "revenue",
        ascending=True,
    )
)

fig_states = go.Figure()

fig_states.add_trace(
    go.Bar(
        x=top_states["revenue"],
        y=top_states["customer_state"],
        orientation="h",
        marker=dict(
            color=[
                "#6475d4",
                "#5687d7",
                "#4e9ed7",
                "#43b1d6",
                "#38bddb",
                "#32c3dd",
                CYAN,
            ]
        ),
        text=[
            f"₹{value:,.0f}"
            for value in top_states["revenue"]
        ],
        textposition="outside",
        textfont=dict(
            color="#b8c7d6",
            size=8,
        ),
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>Revenue: ₹%{x:,.2f}"
            "<extra></extra>"
        ),
    )
)

fig_states.update_layout(
    showlegend=False,
)

fig_states.update_xaxes(
    tickformat=".2s",
)

apply_chart_layout(
    fig_states,
    height=300,
    margin=dict(
        l=35,
        r=62,
        t=5,
        b=30,
    ),
)


# ============================================================
# CUSTOMER GROWTH
# ============================================================

if "customer_id" in orders.columns:

    customer_growth = (
        orders
        .dropna(
            subset=[
                "order_purchase_timestamp",
                "customer_id",
            ]
        )
        .assign(
            order_month=lambda df:
            df["order_purchase_timestamp"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )
        .groupby("order_month")["customer_id"]
        .nunique()
        .reset_index(
            name="monthly_customers"
        )
        .sort_values("order_month")
    )

    # Cumulative unique customer base
    customer_growth["customers"] = (
        customer_growth["monthly_customers"]
        .cumsum()
    )

else:

    customer_growth = pd.DataFrame(
        columns=[
            "order_month",
            "monthly_customers",
            "customers",
        ]
    )


# ============================================================
# CUSTOMER GROWTH CHART
# ============================================================

fig_customer_growth = go.Figure()

if not customer_growth.empty:

    fig_customer_growth.add_trace(
        go.Scatter(
            x=customer_growth["order_month"],
            y=customer_growth["customers"],
            mode="lines",
            line=dict(
                color=PINK,
                width=2.5,
                shape="spline",
            ),
            fill="tozeroy",
            fillcolor="rgba(236,72,153,0.05)",
            hovertemplate=(
                "<b>%{x|%b %Y}</b>"
                "<br>Cumulative Customers: %{y:,}"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

else:

    fig_customer_growth.add_annotation(
        text="Customer growth data unavailable",
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            color=MUTED,
            size=10,
        ),
    )

apply_chart_layout(
    fig_customer_growth,
    height=300,
    margin=dict(
        l=55,
        r=18,
        t=5,
        b=30,
    ),
)


# ============================================================
# SPARKLINE
# ============================================================


# ============================================================
# SPARKLINE
# ============================================================

def create_sparkline(values, color):

    values = pd.Series(values).dropna()

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            y=values.tolist(),
            mode="lines",
            line=dict(
                color=color,
                width=2,
                shape="spline",
            ),
            fill="tozeroy",
            fillcolor="rgba(34,211,238,0.04)",
            hoverinfo="skip",
            showlegend=False,
        )
    )

    figure.update_layout(
        height=45,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            visible=False,
            fixedrange=True,
        ),
        yaxis=dict(
            visible=False,
            fixedrange=True,
        ),
        hovermode=False,
    )

    return figure


# ============================================================
# RECENT ORDERS
# ============================================================

recent_orders = (
    orders
    .dropna(
        subset=[
            "order_purchase_timestamp",
        ]
    )
    .sort_values(
        "order_purchase_timestamp",
        ascending=False,
    )
    .head(7)
    .copy()
)


def build_recent_orders():

    if recent_orders.empty:

        return html.Div(
            "No recent orders available.",
            className="pc-empty-state",
        )

    rows = []

    for _, row in recent_orders.iterrows():

        order_id = str(
            row.get(
                "order_id",
                "N/A",
            )
        )

        order_short = (
            order_id[:10] + "..."
            if len(order_id) > 13
            else order_id
        )

        customer_id = str(
            row.get(
                "customer_id",
                "N/A",
            )
        )

        customer_short = (
            customer_id[:8] + "..."
            if len(customer_id) > 11
            else customer_id
        )

        timestamp = row[
            "order_purchase_timestamp"
        ]

        date_text = pd.to_datetime(
            timestamp
        ).strftime(
            "%d %b %Y",
        )

        status = str(
            row.get(
                "order_status",
                "unknown",
            )
        )

        status_class = (
            "status-success"
            if status == "delivered"
            else "status-warning"
            if status in {
                "shipped",
                "processing",
                "invoiced",
            }
            else "status-danger"
            if status in {
                "canceled",
                "unavailable",
            }
            else "status-info"
        )

        rows.append(
            html.Tr(
                [
                    html.Td(
                        html.Span(
                            order_short,
                            className="order-id",
                        )
                    ),
                    html.Td(date_text),
                    html.Td(
                        html.Span(
                            status.title(),
                            className=(
                                f"status-badge {status_class}"
                            ),
                        )
                    ),
                    html.Td(customer_short),
                ]
            )
        )

    return html.Div(
        html.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th("Order"),
                            html.Th("Date"),
                            html.Th("Status"),
                            html.Th("Customer"),
                        ]
                    )
                ),
                html.Tbody(rows),
            ],
            className="data-table",
        ),
        className="table-scroll",
    )


# ============================================================
# KPI SPARKLINES
# ============================================================

revenue_spark = create_sparkline(
    monthly_sales["revenue"].tail(10),
    CYAN,
)

if "orders" in monthly_sales.columns:

    orders_spark = create_sparkline(
        monthly_sales["orders"].tail(10),
        VIOLET,
    )

else:

    orders_spark = create_sparkline(
        monthly_sales["revenue"].tail(10),
        VIOLET,
    )


if not customer_growth.empty:

    customer_spark = create_sparkline(
        customer_growth["customers"].tail(10),
        PINK,
    )

else:

    customer_spark = create_sparkline(
        monthly_sales["revenue"].tail(10),
        PINK,
    )


aov_spark = create_sparkline(
    monthly_sales["revenue"].tail(10),
    AMBER,
)


# ============================================================
# PAGE LAYOUT
# ============================================================

layout = html.Div(
    [

        # ----------------------------------------------------
        # PAGE HEADER
        # ----------------------------------------------------

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            "EXECUTIVE",
                            className="page-eyebrow",
                        ),

                        html.H1(
                            "Executive Overview",
                            className="page-title",
                        ),

                        html.P(
                            (
                                "Key performance metrics and "
                                "business intelligence from the "
                                "historical e-commerce dataset."
                            ),
                            className="page-subtitle",
                        ),
                    ]
                ),

                create_insight_card(
                    label="Key Insight",
                    title=(
                        f"{top_category} generated "
                        f"{format_millions(top_category_revenue)} "
                        f"and represented "
                        f"{top_category_share:.1f}% "
                        "of category revenue."
                    ),
                    description=(
                        f"The strongest revenue month was "
                        f"{peak_month}, reaching "
                        f"{format_millions(peak_revenue)}."
                    ),
                    icon="✦",
                    variant="violet",
                ),
            ],
            className="exec-header",
        ),


        # ----------------------------------------------------
        # KPI GRID
        # ----------------------------------------------------

        html.Div(
            [
                create_kpi_card(
                    title="Total Revenue",
                    value=format_millions(revenue),
                    icon="₹",
                    variant="cyan",
                    delta=revenue_mom,
                    delta_label="MoM",
                    subtitle="Historical revenue",
                    sparkline=dcc.Graph(
                        figure=revenue_spark,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),
                ),

                create_kpi_card(
                    title="Total Orders",
                    value=format_number(orders_count),
                    icon="◈",
                    variant="violet",
                    subtitle="Completed order records",
                    sparkline=dcc.Graph(
                        figure=orders_spark,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),
                ),

                create_kpi_card(
                    title="Total Customers",
                    value=format_number(customers),
                    icon="●",
                    variant="pink",
                    subtitle="Unique customers",
                    sparkline=dcc.Graph(
                        figure=customer_spark,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),
                ),

                create_kpi_card(
                    title="Average Order Value",
                    value=format_currency(aov),
                    icon="◆",
                    variant="amber",
                    subtitle="Revenue per order",
                    sparkline=dcc.Graph(
                        figure=aov_spark,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    "✓",
                                    className="delivery-icon",
                                ),
                                html.Span(
                                    "Delivery",
                                    className="kpi-label",
                                ),
                            ],
                            className="delivery-header",
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            "On-Time",
                                            className="delivery-label",
                                        ),
                                        html.Div(
                                            format_percent(
                                                on_time_rate
                                            ),
                                            className="delivery-value",
                                        ),
                                        html.Div(
                                            "Delivery performance",
                                            className="delivery-subtitle",
                                        ),
                                    ],
                                    className="delivery-copy",
                                ),

                                html.Div(
                                    html.Span(
                                        f"{on_time_rate:.1f}%",
                                        className="delivery-ring-value",
                                    ),
                                    className="delivery-ring",
                                    style={
                                        "--delivery-progress":
                                            f"{on_time_rate}%"
                                    },
                                ),
                            ],
                            className="delivery-body",
                        ),
                    ],
                    className="kpi-card kpi-card-green",
                ),
            ],
            className="kpi-grid executive-kpi-grid",
        ),


        # ----------------------------------------------------
        # MAIN ANALYTICS
        # ----------------------------------------------------

        html.Div(
            [
                create_chart_card(
                    title="Monthly Revenue Trend",
                    subtitle=(
                        f"Peak: {peak_month} • "
                        f"{format_millions(peak_revenue)}"
                    ),
                    figure=fig_revenue,
                    class_name="exec-revenue-card",
                    height=330,
                ),

                create_chart_card(
                    title="Orders by Status",
                    subtitle="Order composition",
                    figure=fig_status,
                    class_name="exec-status-card",
                    height=330,
                ),
            ],
            className="exec-main-grid",
        ),


        # ----------------------------------------------------
        # SECONDARY ANALYTICS
        # ----------------------------------------------------

        html.Div(
            [
                create_chart_card(
                    title="Top 5 Product Categories",
                    subtitle="Revenue contribution",
                    figure=fig_categories,
                    class_name="exec-category-card",
                    height=300,
                ),

                create_chart_card(
                    title="Revenue by State",
                    subtitle="Top geographic markets",
                    figure=fig_states,
                    class_name="exec-state-card",
                    height=300,
                ),
            ],
            className="exec-secondary-grid",
        ),


        # ----------------------------------------------------
        # CUSTOMER + RECENT ORDERS
        # ----------------------------------------------------

        html.Div(
            [
                create_chart_card(
                    title="Customer Growth",
                    subtitle=(
                        f"{format_number(customers)} "
                        "unique customers"
                    ),
                    figure=fig_customer_growth,
                    class_name="exec-customer-card",
                    height=300,
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    "Recent Orders",
                                    className="chart-card-title",
                                ),
                                html.Div(
                                    "Latest records from the dataset",
                                    className="chart-card-subtitle",
                                ),
                            ],
                            className="chart-card-header",
                        ),

                        build_recent_orders(),
                    ],
                    className="chart-card exec-orders-card",
                ),
            ],
            className="exec-bottom-grid",
        ),


        # ----------------------------------------------------
        # BUSINESS INSIGHTS
        # ----------------------------------------------------

        html.Div(
            [
                create_insight_item(
                    title="Category concentration",
                    description=(
                        f"{top_category} leads category revenue "
                        f"with {format_millions(top_category_revenue)}."
                    ),
                    icon="◆",
                    variant="violet",
                ),

                create_insight_item(
                    title="Customer retention",
                    description=(
                        f"Repeat customer rate is "
                        f"{format_percent(repeat_rate)}."
                    ),
                    icon="●",
                    variant="pink",
                ),

                create_insight_item(
                    title="Delivery performance",
                    description=(
                        f"{format_percent(on_time_rate)} "
                        "of comparable delivered orders "
                        "arrived on or before the estimated date."
                    ),
                    icon="✓",
                    variant="cyan",
                ),
            ],
            className="exec-insights-grid",
        ),


        # ----------------------------------------------------
        # SOURCE FOOTNOTE
        # ----------------------------------------------------

        html.Div(
            [
                html.Span(
                    "Source: Olist Brazilian E-Commerce Public Dataset"
                ),
                html.Span(
                    "Metrics: Validated"
                ),
            ],
            className="page-footnote",
        ),

    ],
    className="executive-page",
)