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

dash.register_page(__name__, path="/customers")


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

CUSTOMER_TYPE_FILE = os.path.join(
    PROCESSED_DIR,
    "customer_type_analysis.csv",
)

RFM_FILE = os.path.join(
    PROCESSED_DIR,
    "rfm_dashboard.csv",
)

CUSTOMER_BEHAVIOR_FILE = os.path.join(
    PROCESSED_DIR,
    "customer_behavior_analysis.csv",
)

COHORT_FILE = os.path.join(
    PROCESSED_DIR,
    "cohort_retention_matrix.csv",
)


# ============================================================
# LOAD DATA
# ============================================================

customer_type = pd.read_csv(CUSTOMER_TYPE_FILE)
rfm = pd.read_csv(RFM_FILE)
customer_behavior = pd.read_csv(CUSTOMER_BEHAVIOR_FILE)
cohort = pd.read_csv(COHORT_FILE)


# ============================================================
# FORMATTING
# ============================================================

def format_number(value):
    return f"{value:,.0f}"


def format_currency(value):
    return f"R${value:,.2f}"


def format_millions(value):
    return f"R${value / 1_000_000:.2f}M"


def format_percent(value):
    return f"{value:.2f}%"


def create_customer_kpi_card(
    title,
    value,
    icon,
    variant,
    subtitle,
    effect_type=None,
    effect_value=None,
    effect_label=None,
    effect_secondary=None,
):
    """
    Customer KPI card with a compact, data-driven micro-visual.

    Effects are semantic:
    - composition: customer mix
    - ring: returning-customer share
    - progress: percentage KPI
    - marker: position of average value in the monetary distribution
    - frequency: purchase-frequency distribution

    No effect represents a historical trend unless a real time series exists.
    """

    card = create_kpi_card(
        title=title,
        value=value,
        icon=icon,
        variant=variant,
        subtitle=subtitle,
    )

    effect = None

    if effect_type == "composition":
        one_time_share = max(
            0.0,
            min(
                float(effect_value or 0),
                100.0,
            ),
        )
        returning_share = max(
            0.0,
            min(
                float(effect_secondary or 0),
                100.0,
            ),
        )

        effect = html.Div(
            [
                html.Div(
                    [
                        html.Span(
                            effect_label or "Customer mix",
                            className="customer-kpi-effect-label",
                        ),
                        html.Span(
                            f"{returning_share:.1f}% returning",
                            className="customer-kpi-effect-value",
                        ),
                    ],
                    className="customer-kpi-effect-meta",
                ),
                html.Div(
                    [
                        html.Div(
                            className="customer-kpi-mix-one-time",
                            style={"width": f"{one_time_share}%"},
                        ),
                        html.Div(
                            className="customer-kpi-mix-returning",
                            style={"width": f"{returning_share}%"},
                        ),
                    ],
                    className="customer-kpi-mix-track",
                ),
            ],
            className="customer-kpi-effect customer-kpi-effect-composition",
        )

    elif effect_type == "ring":
        progress = max(
            0.0,
            min(
                float(effect_value or 0),
                100.0,
            ),
        )

        effect = html.Div(
            [
                html.Div(
                    className="customer-kpi-ring",
                    style={
                        "background": (
                            "radial-gradient(circle at center, "
                            "var(--bg-main) 54%, transparent 56%), "
                            f"conic-gradient(rgba(139, 92, 246, .95) {progress}%, "
                            "rgba(148, 163, 184, .10) 0)"
                        )
                    },
                ),
                html.Div(
                    [
                        html.Span(
                            effect_label or "Share of customers",
                            className="customer-kpi-effect-label",
                        ),
                        html.Span(
                            f"{progress:.2f}%",
                            className="customer-kpi-effect-value",
                        ),
                    ],
                    className="customer-kpi-ring-copy",
                ),
            ],
            className="customer-kpi-effect customer-kpi-effect-ring",
        )

    elif effect_type == "progress":
        progress = max(
            0.0,
            min(
                float(effect_value or 0),
                100.0,
            ),
        )

        effect = html.Div(
            [
                html.Div(
                    [
                        html.Span(
                            effect_label or "Returning rate",
                            className="customer-kpi-effect-label",
                        ),
                        html.Span(
                            f"{progress:.2f}%",
                            className="customer-kpi-effect-value",
                        ),
                    ],
                    className="customer-kpi-effect-meta",
                ),
                html.Div(
                    html.Div(
                        className="customer-kpi-progress-fill",
                        style={"width": f"{progress}%"},
                    ),
                    className="customer-kpi-progress-track",
                ),
            ],
            className="customer-kpi-effect customer-kpi-effect-progress",
        )

    elif effect_type == "marker":
        position = max(
            0.0,
            min(
                float(effect_value or 0),
                100.0,
            ),
        )

        effect = html.Div(
            [
                html.Div(
                    [
                        html.Span(
                            effect_label or "Value position",
                            className="customer-kpi-effect-label",
                        ),
                        html.Span(
                            f"{position:.0f}th pct.",
                            className="customer-kpi-effect-value",
                        ),
                    ],
                    className="customer-kpi-effect-meta",
                ),
                html.Div(
                    [
                        html.Div(
                            className="customer-kpi-marker-line",
                        ),
                        html.Div(
                            className="customer-kpi-marker-dot",
                            style={"left": f"{position}%"},
                        ),
                    ],
                    className="customer-kpi-marker-track",
                ),
            ],
            className="customer-kpi-effect customer-kpi-effect-marker",
        )

    elif effect_type == "frequency":
        values = list(effect_value or [])
        max_value = max(values) if values else 1

        effect = html.Div(
            [
                html.Div(
                    [
                        html.Span(
                            effect_label or "Purchase mix",
                            className="customer-kpi-effect-label",
                        ),
                        html.Span(
                            effect_secondary or "1+ order distribution",
                            className="customer-kpi-effect-value",
                        ),
                    ],
                    className="customer-kpi-effect-meta",
                ),
                html.Div(
                    [
                        html.Div(
                            className="customer-kpi-frequency-bar",
                            style={
                                "height": (
                                    f"{max(8, (value / max_value) * 100):.1f}%"
                                ),
                            },
                        )
                        for value in values
                    ],
                    className="customer-kpi-frequency-bars",
                ),
            ],
            className="customer-kpi-effect customer-kpi-effect-frequency",
        )

    if effect is None:
        return card

    return html.Div(
        [
            card,
            effect,
        ],
        className="customer-kpi-wrapper",
    )


# ============================================================
# CUSTOMER KPIs
# ============================================================

# ============================================================

total_customers = int(
    customer_type["customers"].sum()
)

returning_row = customer_type[
    customer_type["customer_type"]
    == "Returning Customer"
]

one_time_row = customer_type[
    customer_type["customer_type"]
    == "One-Time Customer"
]

returning_customers = (
    int(returning_row["customers"].iloc[0])
    if not returning_row.empty
    else 0
)

one_time_customers = (
    int(one_time_row["customers"].iloc[0])
    if not one_time_row.empty
    else 0
)

repeat_rate = (
    returning_customers
    / total_customers
    * 100
    if total_customers
    else 0
)

average_customer_value = float(
    rfm["monetary"].mean()
)

average_orders = float(
    customer_behavior["order_count"].mean()
)


# ============================================================
# RFM SUMMARY
# ============================================================

rfm_summary = (
    rfm
    .groupby("segment", as_index=False)
    .agg(
        customers=(
            "customer_unique_id",
            "count",
        ),
        revenue=(
            "monetary",
            "sum",
        ),
    )
)

rfm_summary["share"] = (
    rfm_summary["customers"]
    / total_customers
    * 100
    if total_customers
    else 0
)

rfm_summary = rfm_summary.sort_values(
    "customers",
    ascending=False,
)


RFM_COLORS = {
    "Champions": "#a78bfa",
    "Loyal Customers": "#8b5cf6",
    "Potential Loyalists": "#22d3ee",
    "High Value New Customers": "#ec4899",
    "High Value At Risk": "#f59e0b",
    "At Risk": "#fb7185",
    "Inactive": "#64748b",
}


# ============================================================
# CUSTOMER TYPE CHART
# ============================================================

customer_type_chart = customer_type.copy()

customer_type_chart["display_type"] = (
    customer_type_chart["customer_type"]
    .replace(
        {
            "One-Time Customer": "One-Time",
            "Returning Customer": "Returning",
        }
    )
)

fig_customer_type = go.Figure()

fig_customer_type.add_trace(
    go.Pie(
        labels=customer_type_chart["display_type"],
        values=customer_type_chart["customers"],
        hole=0.70,
        pull=[0.012, 0.0],
        sort=False,
        marker=dict(
            colors=[
                "#8b5cf6",
                "#ec4899",
            ],
            line=dict(
                color="#09111d",
                width=3,
            ),
        ),
        textinfo="none",
        hovertemplate=(
            "<b>%{label}</b>"
            "<br>Customers: %{value:,}"
            "<br>Share: %{percent}"
            "<extra></extra>"
        ),
    )
)

fig_customer_type.add_annotation(
    text=(
        f"<b>{format_number(total_customers)}</b>"
        "<br>"
        "<span style='font-size:9px'>Customers</span>"
    ),
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(
        color="#f1f5f9",
        size=17,
    ),
)

fig_customer_type.update_layout(
    showlegend=True,
    legend=dict(
        orientation="h",
        x=0.5,
        xanchor="center",
        y=-0.02,
        font=dict(
            color="#a9b8c9",
            size=9,
        ),
    ),
)

fig_customer_type.update_layout(
    template="analytics_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=290,
    margin=dict(
        l=10,
        r=10,
        t=5,
        b=25,
    ),
)


# ============================================================
# RFM REVENUE
# ============================================================

rfm_revenue = (
    rfm_summary
    .sort_values(
        "revenue",
        ascending=True,
    )
)

fig_rfm_revenue = go.Figure()

fig_rfm_revenue.add_trace(
    go.Bar(
        x=rfm_revenue["revenue"],
        y=rfm_revenue["segment"],
        orientation="h",
        marker=dict(
            color=[
                RFM_COLORS.get(
                    segment,
                    "#8b5cf6",
                )
                for segment
                in rfm_revenue["segment"]
            ],
            line=dict(width=0),
        ),
        text=rfm_revenue["revenue"],
        texttemplate="R$%{text:,.0f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>Revenue: R$%{x:,.2f}"
            "<extra></extra>"
        ),
    )
)

fig_rfm_revenue.update_layout(
    template="analytics_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=300,
    margin=dict(
        l=145,
        r=100,
        t=10,
        b=25,
    ),
    showlegend=False,
)

fig_rfm_revenue.update_xaxes(
    showgrid=True,
    gridcolor="rgba(148,163,184,0.075)",
    zeroline=False,
    tickfont=dict(
        color="#708198",
        size=8,
    ),
    tickformat=".2s",
)

fig_rfm_revenue.update_yaxes(
    showgrid=False,
    tickfont=dict(
        color="#a9b8c9",
        size=8,
    ),
)


# ============================================================
# PURCHASE FREQUENCY
# ============================================================

frequency = (
    customer_behavior[
        "purchase_frequency_group"
    ]
    .value_counts()
    .reset_index()
)

frequency.columns = [
    "frequency_group",
    "customers",
]

frequency = frequency.sort_values(
    "customers",
    ascending=True,
)

frequency_colors = [
    "#6475d4",
    "#8177db",
    "#8b5cf6",
    "#ec4899",
]

fig_frequency = go.Figure()

fig_frequency.add_trace(
    go.Bar(
        x=frequency["customers"],
        y=frequency["frequency_group"],
        orientation="h",
        marker=dict(
            color=(
                frequency_colors[
                    :len(frequency)
                ]
            ),
        ),
        text=frequency["customers"],
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>Customers: %{x:,}"
            "<extra></extra>"
        ),
    )
)

fig_frequency.update_layout(
    template="analytics_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=300,
    margin=dict(
        l=110,
        r=75,
        t=10,
        b=25,
    ),
    showlegend=False,
)

fig_frequency.update_xaxes(
    showgrid=True,
    gridcolor="rgba(148,163,184,0.075)",
    zeroline=False,
    tickfont=dict(
        color="#708198",
        size=8,
    ),
)

fig_frequency.update_yaxes(
    showgrid=False,
    tickfont=dict(
        color="#a9b8c9",
        size=8,
    ),
)

# ============================================================
# COHORT RETENTION
# ============================================================

cohort_chart = cohort.copy()

cohort_chart["cohort_month"] = pd.to_datetime(
    cohort_chart["cohort_month"],
    errors="coerce",
)

cohort_chart = (
    cohort_chart
    .dropna(subset=["cohort_month"])
    .sort_values("cohort_month")
)

cohort_chart["cohort_label"] = (
    cohort_chart["cohort_month"]
    .dt.strftime("%b %Y")
)

retention_columns = [
    column
    for column in cohort_chart.columns
    if column not in [
        "cohort_month",
        "cohort_label",
    ]
]

# Convert retention values to numeric
for column in retention_columns:
    cohort_chart[column] = pd.to_numeric(
        cohort_chart[column],
        errors="coerce",
    )

# Ensure month columns are ordered numerically
def month_sort_key(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 999


retention_columns = sorted(
    retention_columns,
    key=month_sort_key,
)

# Build heatmap matrix
z_values = cohort_chart[
    retention_columns
].to_numpy(dtype=float)

y_labels = cohort_chart[
    "cohort_label"
].tolist()

x_labels = [
    f"M{month}"
    for month in retention_columns
]


# ============================================================
# COHORT HEATMAP
# ============================================================

fig_cohort = go.Figure()

if len(z_values) > 0:

    # Display values inside cells.
    text_values = []

    for row in z_values:

        text_row = []

        for value in row:

            if pd.isna(value):
                text_row.append("")
            else:
                text_row.append(
                    f"{value:.0f}%"
                )

        text_values.append(text_row)

    fig_cohort.add_trace(
        go.Heatmap(
            z=z_values,
            x=x_labels,
            y=y_labels,
            text=text_values,
            texttemplate="%{text}",
            textfont=dict(
                color="#eef2ff",
                size=8,
            ),
            colorscale=[
                [0.00, "#101827"],
                [0.10, "#17142d"],
                [0.25, "#292052"],
                [0.45, "#493078"],
                [0.65, "#7040a2"],
                [0.82, "#a24dbb"],
                [1.00, "#ec4899"],
            ],
            zmin=0,
            zmax=100,
            xgap=3,
            ygap=3,
            hoverongaps=False,
            hoverlabel=dict(bgcolor="#0b1524", font=dict(color="#eef2ff")),
            colorbar=dict(
                title=dict(
                    text="Retention",
                    font=dict(
                        color="#91a4b8",
                        size=9,
                    ),
                ),
                ticksuffix="%",
                tickfont=dict(
                    color="#91a4b8",
                    size=8,
                ),
                thickness=10,
                len=0.72,
            ),
            hovertemplate=(
                "<b>%{y}</b>"
                "<br>%{x}"
                "<br>Retention: %{z:.2f}%"
                "<extra></extra>"
            ),
        )
    )

else:

    fig_cohort.add_annotation(
        text="Cohort retention data unavailable",
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


fig_cohort.update_layout(
    template="analytics_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=335,
    margin=dict(
        l=68,
        r=55,
        t=10,
        b=45,
    ),
    showlegend=False,
)


fig_cohort.update_xaxes(
    title=dict(
        text="Months Since First Purchase",
        font=dict(
            color="#708198",
            size=9,
        ),
    ),
    tickmode="array",
    tickvals=x_labels,
    ticktext=x_labels,
    showgrid=False,
    zeroline=False,
    tickfont=dict(
        color="#91a4b8",
        size=8,
    ),
)


fig_cohort.update_yaxes(
    title=None,
    autorange="reversed",
    showgrid=False,
    zeroline=False,
    tickfont=dict(
        color="#91a4b8",
        size=8,
    ),
)


# ============================================================
# RFM SEGMENT COLORS
# ============================================================

def rfm_color(segment):
    return RFM_COLORS.get(
        str(segment),
        "#8b5cf6",
    )


# ============================================================
# RFM SEGMENT ITEMS
# ============================================================

def create_rfm_item(row):

    segment = str(row["segment"])
    color = rfm_color(segment)

    return html.Div(
        [
            html.Div(
                [
                    html.Span(
                        className="rfm-dot",
                        style={
                            "backgroundColor": color,
                            "boxShadow": (
                                f"0 0 10px {color}"
                            ),
                        },
                    ),

                    html.Span(
                        segment,
                        className="rfm-name",
                    ),
                ],
                className="rfm-item-heading",
            ),

            html.Div(
                format_number(
                    row["customers"]
                ),
                className="rfm-count",
            ),

            html.Div(
                [
                    html.Span(
                        f"{row['share']:.1f}% of customers"
                    ),
                    html.Span(
                        format_millions(
                            row["revenue"]
                        )
                    ),
                ],
                className="rfm-item-meta",
            ),
        ],
        className="rfm-item",
    )


rfm_items = [
    create_rfm_item(row)
    for _, row in rfm_summary.iterrows()
]


# ============================================================
# CUSTOMER INSIGHTS
# ============================================================

top_rfm = (
    rfm_summary
    .sort_values(
        "revenue",
        ascending=False,
    )
    .iloc[0]
)

largest_segment = (
    rfm_summary
    .sort_values(
        "customers",
        ascending=False,
    )
    .iloc[0]
)


# ============================================================
# KPI MICRO-VISUAL REFERENCES
# ============================================================

returning_share = (
    returning_customers
    / total_customers
    * 100
    if total_customers
    else 0
)

one_time_share = (
    one_time_customers
    / total_customers
    * 100
    if total_customers
    else 0
)

# Empirical percentile of the average RFM monetary value.
# This describes where the average sits in the customer-value
# distribution without pretending to be a time trend.
if not rfm.empty and "monetary" in rfm.columns:
    value_position = (
        rfm["monetary"]
        .le(average_customer_value)
        .mean()
        * 100
    )
else:
    value_position = 0

frequency_distribution = (
    customer_behavior[
        "purchase_frequency_group"
    ]
    .value_counts()
    .sort_index()
    .tolist()
)


# ============================================================
# PAGE LAYOUT
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
                            "CUSTOMERS",
                            className="page-eyebrow",
                        ),

                        html.H1(
                            "Customer Intelligence",
                            className="page-title",
                        ),

                        html.P(
                            (
                                "Customer value, retention, "
                                "segmentation and purchase "
                                "behavior from the historical dataset."
                            ),
                            className="page-description",
                        ),
                    ],
                    className="customers-header-copy",
                ),

                create_insight_card(
                    label="Key Insight",
                    title=(
                        f"{top_rfm['segment']} generates "
                        f"{format_millions(top_rfm['revenue'])} "
                        "in customer value."
                    ),
                    description=(
                        f"{format_number(top_rfm['customers'])} "
                        f"customers belong to this segment, while "
                        f"returning customers represent "
                        f"{repeat_rate:.2f}% of the customer base."
                    ),
                    icon="✦",
                    variant="violet",
                ),
            ],
            className="customers-header",
        ),


        # ====================================================
        # KPI GRID
        # ====================================================

        html.Div(
            [
                create_customer_kpi_card(
                    title="Total Customers",
                    value=format_number(total_customers),
                    icon="●",
                    variant="cyan",
                    subtitle="Unique customer base",
                    effect_type="composition",
                    effect_value=one_time_share,
                    effect_secondary=returning_share,
                    effect_label="Customer mix",
                ),

                create_customer_kpi_card(
                    title="Returning Customers",
                    value=format_number(returning_customers),
                    icon="↻",
                    variant="violet",
                    subtitle="Customers with repeat purchases",
                    effect_type="ring",
                    effect_value=returning_share,
                    effect_label="Share of customers",
                ),

                create_customer_kpi_card(
                    title="Repeat Customer Rate",
                    value=format_percent(repeat_rate),
                    icon="%",
                    variant="pink",
                    subtitle="Returning / total customers",
                    effect_type="progress",
                    effect_value=repeat_rate,
                    effect_label="Returning rate",
                ),

                create_customer_kpi_card(
                    title="Average Customer Value",
                    value=format_currency(
                        average_customer_value
                    ),
                    icon="R$",
                    variant="amber",
                    subtitle="Average RFM monetary value",
                    effect_type="marker",
                    effect_value=value_position,
                    effect_label="Customer value position",
                ),

                create_customer_kpi_card(
                    title="Avg Orders / Customer",
                    value=f"{average_orders:.2f}",
                    icon="↗",
                    variant="cyan",
                    subtitle="Average purchase frequency",
                    effect_type="frequency",
                    effect_value=frequency_distribution,
                    effect_label="Purchase mix",
                    effect_secondary="1+ order distribution",
                ),
            ],
            className="kpi-grid customers-kpi-grid",
        ),


        # ====================================================
        # COHORT + CUSTOMER TYPE
        # ====================================================

        html.Div(
            [
                create_chart_card(
                    title="Cohort Retention",
                    subtitle=(
                        "Retention across months since first purchase"
                    ),
                    figure=fig_cohort,
                    class_name="customers-cohort-card",
                    height=335,
                ),

                create_chart_card(
                    title="Customer Type",
                    subtitle="One-time vs returning customers",
                    figure=fig_customer_type,
                    class_name="customers-type-card",
                    height=290,
                ),
            ],
            className="customers-main-grid",
        ),


        # ====================================================
        # RFM SEGMENTS
        # ====================================================

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            "RFM SEGMENTATION",
                            className="section-eyebrow",
                        ),

                        html.Div(
                            "Customer value and engagement profile across RFM segments",
                            className="section-subtitle",
                        ),
                    ],
                    className="customers-section-heading",
                ),

                html.Div(
                    rfm_items,
                    className="rfm-grid",
                ),
            ],
            className="customers-rfm-section",
        ),


        # ====================================================
        # RFM REVENUE + PURCHASE FREQUENCY
        # ====================================================

        html.Div(
            [
                create_chart_card(
                    title="Revenue by RFM Segment",
                    subtitle="Customer value contribution",
                    figure=fig_rfm_revenue,
                    class_name="customers-rfm-revenue",
                    height=300,
                ),

                create_chart_card(
                    title="Purchase Frequency",
                    subtitle="Distribution of customer purchase behavior",
                    figure=fig_frequency,
                    class_name="customers-frequency",
                    height=300,
                ),
            ],
            className="customers-secondary-grid",
        ),


        # ====================================================
        # BUSINESS INSIGHTS
        # ====================================================

        html.Div(
            [
                create_insight_item(
                    title="Largest customer segment",
                    description=(
                        f"{largest_segment['segment']} contains "
                        f"{format_number(largest_segment['customers'])} "
                        f"customers, representing "
                        f"{largest_segment['share']:.1f}% "
                        "of the customer base."
                    ),
                    icon="●",
                    variant="cyan",
                ),

                create_insight_item(
                    title="Customer retention",
                    description=(
                        f"Returning customers account for "
                        f"{repeat_rate:.2f}% of customers."
                    ),
                    icon="↻",
                    variant="pink",
                ),

                create_insight_item(
                    title="Highest-value segment",
                    description=(
                        f"{top_rfm['segment']} contributes "
                        f"{format_millions(top_rfm['revenue'])} "
                        "in RFM monetary value."
                    ),
                    icon="◆",
                    variant="violet",
                ),
            ],
            className="customers-insights-grid",
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
                    "Customer analytics: Validated"
                ),
            ],
            className="page-footnote",
        ),

    ],
    className="customers-page",
)