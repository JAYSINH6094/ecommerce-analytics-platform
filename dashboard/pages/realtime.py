import requests
import pandas as pd
import plotly.graph_objects as go

import dash
from dash import (
    html,
    dcc,
    Input,
    Output,
    callback,
)

from dashboard import plotly_theme


# ============================================================
# PAGE REGISTRATION
# ============================================================

dash.register_page(
    __name__,
    path="/realtime",
    name="Real-Time",
)


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"

REFRESH_INTERVAL = 10 * 1000


# ============================================================
# API HELPER
# ============================================================

def get_api_data(endpoint):
    """
    Safely fetch JSON data from FastAPI.
    """

    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}",
            timeout=5,
        )

        response.raise_for_status()

        return response.json()

    except (
        requests.RequestException,
        ValueError,
        TypeError,
    ):
        return None


# ============================================================
# GENERIC HELPERS
# ============================================================

def first_value(data, keys, default=0):

    if not isinstance(data, dict):
        return default

    for key in keys:

        if (
            key in data
            and data[key] is not None
        ):
            return data[key]

    return default


def safe_float(value, default=0.0):

    try:

        if value is None:
            return default

        return float(value)

    except (
        ValueError,
        TypeError,
    ):
        return default


def safe_int(value, default=0):

    try:

        if value is None:
            return default

        return int(float(value))

    except (
        ValueError,
        TypeError,
    ):
        return default


def extract_rows(
    payload,
    possible_keys,
):

    if isinstance(payload, list):
        return payload

    if not isinstance(payload, dict):
        return []

    for key in possible_keys:

        value = payload.get(key)

        if isinstance(value, list):
            return value

    return []


def get_order_amount(row):

    if not isinstance(row, dict):
        return 0.0

    for key in [
        "order_value",
        "total",
        "total_value",
        "revenue",
        "amount",
        "total_revenue",
    ]:

        if key in row:

            value = safe_float(
                row.get(key),
                None,
            )

            if value is not None:
                return value

    price = safe_float(
        row.get("price"),
        0,
    )

    quantity = safe_float(
        row.get("quantity"),
        1,
    )

    freight = safe_float(
        row.get("freight_value"),
        0,
    )

    if price != 0:

        return (
            price * quantity
            + freight
        )

    return 0.0


def get_order_items(row):

    if not isinstance(row, dict):
        return 0

    for key in [
        "quantity",
        "items",
        "item_count",
        "total_items",
    ]:

        if key in row:

            return safe_int(
                row.get(key),
                0,
            )

    return 0


def get_order_id(row):

    if not isinstance(row, dict):
        return "Unknown"

    for key in [
        "order_id",
        "id",
        "transaction_id",
    ]:

        if key in row:

            value = row.get(key)

            if value is not None:
                return str(value)

    return "Unknown"


def get_customer_id(row):

    if not isinstance(row, dict):
        return ""

    for key in [
        "customer_id",
        "customer_unique_id",
    ]:

        if key in row:

            value = row.get(key)

            if value is not None:
                return str(value)

    return ""


def get_category(row):

    if not isinstance(row, dict):
        return "Unknown"

    for key in [
        "product_category",
        "product_category_name",
        "category",
        "category_name",
    ]:

        if key in row:

            value = row.get(key)

            if value:

                return str(value).replace(
                    "_",
                    " ",
                ).title()

    return "Unknown"


def get_state(row):

    if not isinstance(row, dict):
        return "Unknown"

    for key in [
        "customer_state",
        "state",
        "region",
    ]:

        if key in row:

            value = row.get(key)

            if value:
                return str(value).upper()

    return "Unknown"


# ============================================================
# EVENT TIMESTAMP HELPERS
# ============================================================

def get_order_timestamp(row):

    if not isinstance(row, dict):
        return None

    for key in [
        "order_timestamp",
        "timestamp",
        "created_at",
        "event_timestamp",
    ]:

        value = row.get(key)

        if value:
            try:
                parsed = pd.to_datetime(
                    value,
                    errors="coerce",
                )

                if pd.notna(parsed):
                    return parsed
            except (TypeError, ValueError):
                pass

    return None


def format_event_time(value):

    timestamp = get_order_timestamp(value)

    if timestamp is None:
        return "Time unavailable"

    return timestamp.strftime("%d %b %Y · %H:%M:%S")


def empty_activity_chart(message="No recent activity available"):

    fig = go.Figure()
    fig.update_layout(
        template="analytics_dark",
        height=280,
        margin=dict(l=12, r=18, t=12, b=34),
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[dict(
            text=message,
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(color="#60748c", size=11),
        )],
    )
    return fig


def create_recent_activity_chart(rows):

    if not isinstance(rows, list) or not rows:
        return empty_activity_chart("No recent activity available")

    labels = []
    values = []
    customdata = []

    for index, row in enumerate(rows[:20], start=1):
        if not isinstance(row, dict):
            continue

        labels.append(str(index))
        values.append(float(get_order_amount(row)))
        customdata.append([
            get_order_id(row),
            get_category(row),
            get_state(row),
        ])

    if not labels:
        return empty_activity_chart("No recent activity available")

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Recent order: %{x}<br>"
                "Revenue: R$ %{y:,.2f}<br>"
                "Category: %{customdata[1]}<br>"
                "State: %{customdata[2]}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        template="analytics_dark",
        height=280,
        margin=dict(l=12, r=18, t=8, b=34),
        showlegend=False,
        xaxis=dict(
            title="Recent order",
            showgrid=False,
            zeroline=False,
            fixedrange=True,
        ),
        yaxis=dict(
            title="Revenue",
            showgrid=True,
            zeroline=False,
            tickprefix="R$ ",
            fixedrange=True,
        ),
    )

    return fig


# ============================================================
# SPARKLINE
# ============================================================

def empty_sparkline():

    fig = go.Figure()

    fig.update_layout(
        template="analytics_dark",
        height=72,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0,
        ),
        xaxis=dict(
            visible=False,
        ),
        yaxis=dict(
            visible=False,
        ),
        showlegend=False,
        hovermode=False,
    )

    return fig


def create_revenue_sparkline(rows):

    if not rows:
        return empty_sparkline()

    values = []

    for row in rows:

        amount = get_order_amount(row)

        if amount >= 0:
            values.append(amount)

    if not values:
        return empty_sparkline()

    values = values[:12]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(
                range(
                    len(values)
                )
            ),
            y=values,
            mode="lines",
            line=dict(
                color="#22d3ee",
                width=2.5,
                shape="spline",
            ),
            fill="tozeroy",
            fillcolor=(
                "rgba(34,211,238,0.07)"
            ),
            hovertemplate=(
                "Revenue: "
                "R$%{y:,.2f}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        template="analytics_dark",
        height=72,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0,
        ),
        xaxis=dict(
            visible=False,
            fixedrange=True,
        ),
        yaxis=dict(
            visible=False,
            fixedrange=True,
        ),
        showlegend=False,
        hovermode="closest",
    )

    return fig


# ============================================================
# ORDER FEED
# ============================================================

def build_order_feed(rows):

    if not rows:

        return html.Div(
            [

                html.Div(
                    "◌",
                    className=(
                        "rt-empty-icon"
                    ),
                ),

                html.Div(
                    "No recent orders",
                    className=(
                        "rt-empty-title"
                    ),
                ),

                html.Div(
                    (
                        "New transactions will appear "
                        "here automatically when the "
                        "FastAPI service receives them."
                    ),
                    className=(
                        "rt-empty-text"
                    ),
                ),

            ],
            className="rt-empty-state",
        )

    feed_rows = []

    for index, row in enumerate(
        rows[:10]
    ):

        order_id = get_order_id(
            row
        )

        customer_id = get_customer_id(
            row
        )

        category = get_category(
            row
        )

        state = get_state(
            row
        )

        amount = get_order_amount(
            row
        )

        quantity = get_order_items(
            row
        )

        meta_parts = []

        if category != "Unknown":
            meta_parts.append(
                category
            )

        if state != "Unknown":
            meta_parts.append(
                state
            )

        if quantity:
            meta_parts.append(
                f"{quantity} item"
                + (
                    "s"
                    if quantity != 1
                    else ""
                )
            )

        if customer_id:
            meta_parts.append(
                f"Customer "
                f"{customer_id[:8]}"
            )

        timestamp = get_order_timestamp(row)

        if timestamp is not None:
            meta_parts.append(
                timestamp.strftime("%d %b %H:%M")
            )

        metadata = " · ".join(
            meta_parts
        )

        if not metadata:
            metadata = "Live transaction"

        row_class = (
            "rt-order-row "
            "rt-order-new"
            if index == 0
            else "rt-order-row"
        )

        feed_rows.append(
            html.Div(
                [

                    html.Div(
                        className=(
                            "rt-order-status-dot"
                        ),
                    ),

                    html.Div(
                        [

                            html.Div(
                                order_id,
                                className=(
                                    "rt-order-id"
                                ),
                            ),

                            html.Div(
                                metadata,
                                className=(
                                    "rt-order-meta"
                                ),
                            ),

                        ],
                        className=(
                            "rt-order-info"
                        ),
                    ),

                    html.Div(
                        f"R${amount:,.2f}",
                        className=(
                            "rt-order-value"
                        ),
                    ),

                ],
                className=row_class,
            )
        )

    return html.Div(
        feed_rows,
        className="rt-order-feed",
    )


# ============================================================
# PAGE LAYOUT
# ============================================================

layout = html.Div(
    [

        # ----------------------------------------------------
        # REFRESH
        # ----------------------------------------------------

        dcc.Interval(
            id="realtime-refresh",
            interval=REFRESH_INTERVAL,
            n_intervals=0,
        ),


        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        html.Div(
            [

                html.Div(
                    [

                        html.Div(
                            "REAL-TIME",
                            className=(
                                "page-eyebrow"
                            ),
                        ),

                        html.H1(
                            "Live Commerce Activity",
                            className=(
                                "page-title"
                            ),
                        ),

                        html.P(
                            (
                                "Monitor orders flowing "
                                "through the FastAPI "
                                "real-time ingestion "
                                "service as they arrive."
                            ),
                            className=(
                                "page-subtitle"
                            ),
                        ),

                    ],
                ),

                html.Div(
                    [

                        html.Span(
                            className=(
                                "rt-live-dot"
                            ),
                        ),

                        html.Span(
                            "LIVE",
                        ),

                    ],
                    className=(
                        "rt-live-pill"
                    ),
                ),

            ],
            className="rt-header",
        ),


        # ----------------------------------------------------
        # KPI GRID
        # ----------------------------------------------------

        html.Div(
            [

                html.Div(
                    [

                        html.Div(
                            [

                                html.Div(
                                    "TODAY'S REVENUE",
                                    className=(
                                        "rt-kpi-label"
                                    ),
                                ),

                                html.Div(
                                    "LIVE",
                                    className=(
                                        "rt-kpi-live-label"
                                    ),
                                ),

                            ],
                            className=(
                                "rt-kpi-top"
                            ),
                        ),

                        html.Div(
                            "R$0.00",
                            id="rt-revenue",
                            className=(
                                "rt-kpi-value"
                            ),
                        ),

                        html.Div(
                            [

                                dcc.Graph(
                                    id=(
                                        "rt-revenue-sparkline"
                                    ),
                                    figure=(
                                        empty_sparkline()
                                    ),
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
                                ),

                            ],
                            className=(
                                "rt-sparkline"
                            ),
                        ),

                    ],
                    className=(
                        "rt-kpi "
                        "rt-kpi-revenue"
                    ),
                ),


                html.Div(
                    [

                        html.Div(
                            "ORDERS",
                            className=(
                                "rt-kpi-label"
                            ),
                        ),

                        html.Div(
                            "◈",
                            className=(
                                "rt-kpi-icon "
                                "rt-icon-violet"
                            ),
                        ),

                        html.Div(
                            "0",
                            id="rt-orders",
                            className=(
                                "rt-kpi-value"
                            ),
                        ),

                        html.Div(
                            "Transactions received",
                            className=(
                                "rt-kpi-subtitle"
                            ),
                        ),

                    ],
                    className="rt-kpi",
                ),


                html.Div(
                    [

                        html.Div(
                            "ITEMS SOLD",
                            className=(
                                "rt-kpi-label"
                            ),
                        ),

                        html.Div(
                            "▦",
                            className=(
                                "rt-kpi-icon "
                                "rt-icon-cyan"
                            ),
                        ),

                        html.Div(
                            "0",
                            id="rt-items",
                            className=(
                                "rt-kpi-value"
                            ),
                        ),

                        html.Div(
                            "Units received",
                            className=(
                                "rt-kpi-subtitle"
                            ),
                        ),

                    ],
                    className="rt-kpi",
                ),


                html.Div(
                    [

                        html.Div(
                            "AVERAGE ORDER VALUE",
                            className=(
                                "rt-kpi-label"
                            ),
                        ),

                        html.Div(
                            "R$",
                            className=(
                                "rt-kpi-icon "
                                "rt-icon-amber"
                            ),
                        ),

                        html.Div(
                            "R$0.00",
                            id="rt-aov",
                            className=(
                                "rt-kpi-value"
                            ),
                        ),

                        html.Div(
                            "Revenue per order",
                            className=(
                                "rt-kpi-subtitle"
                            ),
                        ),

                    ],
                    className="rt-kpi",
                ),

            ],
            className="rt-kpi-grid",
        ),


        # ----------------------------------------------------
        # MAIN CONTENT
        # ----------------------------------------------------

        html.Div(
            [

                # ==================================================
                # RECENT ORDERS
                # ==================================================

                html.Div(
                    [

                        html.Div(
                            [

                                html.Div(
                                    [

                                        html.Div(
                                            "TRANSACTION STREAM",
                                            className=(
                                                "rt-panel-eyebrow"
                                            ),
                                        ),

                                        html.H2(
                                            "Recent Orders",
                                            className=(
                                                "rt-panel-title"
                                            ),
                                        ),

                                    ],
                                ),

                                html.Div(
                                    "● Live · Waiting for first refresh",
                                    id="rt-last-update",
                                    className=(
                                        "rt-update-label"
                                    ),
                                ),

                            ],
                            className=(
                                "rt-panel-header"
                            ),
                        ),

                        html.Div(
                            id="rt-order-feed",
                            className=(
                                "rt-order-feed-container"
                            ),
                        ),

                        html.Div(
                            [
                                html.Div(
                                    "RECENT ACTIVITY",
                                    className="rt-activity-label",
                                ),
                                dcc.Graph(
                                    id="rt-activity-chart",
                                    figure=create_recent_activity_chart([]),
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
                                ),
                            ],
                            className="rt-activity-wrap",
                        ),

                    ],
                    className=(
                        "rt-panel "
                        "rt-orders-panel"
                    ),
                ),


                # ==================================================
                # PIPELINE
                # ==================================================

                html.Div(
                    [

                        html.Div(
                            "SYSTEM",
                            className=(
                                "rt-panel-eyebrow"
                            ),
                        ),

                        html.H2(
                            "Pipeline Status",
                            className=(
                                "rt-panel-title"
                            ),
                        ),

                        html.Div(
                            [

                                html.Div(
                                    [

                                        html.Div(
                                            className=(
                                                "rt-pipeline-dot "
                                                "online"
                                            ),
                                        ),

                                        html.Div(
                                            [

                                                html.Div(
                                                    "FastAPI",
                                                    className=(
                                                        "rt-pipeline-name"
                                                    ),
                                                ),

                                                html.Div(
                                                    "Order ingestion API",
                                                    className=(
                                                        "rt-pipeline-meta"
                                                    ),
                                                ),

                                            ],
                                        ),

                                        html.Div(
                                            "ONLINE",
                                            className=(
                                                "rt-pipeline-status"
                                            ),
                                        ),

                                    ],
                                    className=(
                                        "rt-pipeline-row"
                                    ),
                                ),


                                html.Div(
                                    className=(
                                        "rt-pipeline-line"
                                    ),
                                ),


                                html.Div(
                                    [

                                        html.Div(
                                            className=(
                                                "rt-pipeline-dot "
                                                "online"
                                            ),
                                        ),

                                        html.Div(
                                            [

                                                html.Div(
                                                    "MySQL",
                                                    className=(
                                                        "rt-pipeline-name"
                                                    ),
                                                ),

                                                html.Div(
                                                    "Real-time order storage",
                                                    className=(
                                                        "rt-pipeline-meta"
                                                    ),
                                                ),

                                            ],
                                        ),

                                        html.Div(
                                            "ONLINE",
                                            className=(
                                                "rt-pipeline-status"
                                            ),
                                        ),

                                    ],
                                    className=(
                                        "rt-pipeline-row"
                                    ),
                                ),


                                html.Div(
                                    className=(
                                        "rt-pipeline-line"
                                    ),
                                ),


                                html.Div(
                                    [

                                        html.Div(
                                            className=(
                                                "rt-pipeline-dot "
                                                "online"
                                            ),
                                        ),

                                        html.Div(
                                            [

                                                html.Div(
                                                    "Dash",
                                                    className=(
                                                        "rt-pipeline-name"
                                                    ),
                                                ),

                                                html.Div(
                                                    "Analytics interface",
                                                    className=(
                                                        "rt-pipeline-meta"
                                                    ),
                                                ),

                                            ],
                                        ),

                                        html.Div(
                                            "ONLINE",
                                            className=(
                                                "rt-pipeline-status"
                                            ),
                                        ),

                                    ],
                                    className=(
                                        "rt-pipeline-row"
                                    ),
                                ),

                            ],
                            className=(
                                "rt-pipeline"
                            ),
                        ),


                        html.Div(
                            [

                                html.Div(
                                    "↗",
                                    className=(
                                        "rt-flow-icon"
                                    ),
                                ),

                                html.Div(
                                    [

                                        html.Div(
                                            "DATA FLOW",
                                            className=(
                                                "rt-flow-label"
                                            ),
                                        ),

                                        html.Div(
                                            (
                                                "FastAPI → MySQL "
                                                "→ Dash analytics"
                                            ),
                                            className=(
                                                "rt-flow-text"
                                            ),
                                        ),

                                    ],
                                ),

                            ],
                            className=(
                                "rt-flow-card"
                            ),
                        ),

                    ],
                    className=(
                        "rt-panel "
                        "rt-pipeline-panel"
                    ),
                ),

            ],
            className="rt-main-grid",
        ),


        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        html.Div(
            [

                html.Span(
                    "Source: FastAPI real-time ingestion service",
                ),

                html.Span(
                    "Refresh interval: 10 seconds",
                ),

            ],
            className="page-footnote",
        ),

    ],
    className="realtime-page",
)


# ============================================================
# SINGLE REAL-TIME CALLBACK
# ============================================================

@callback(
    Output(
        "rt-revenue",
        "children",
    ),

    Output(
        "rt-orders",
        "children",
    ),

    Output(
        "rt-items",
        "children",
    ),

    Output(
        "rt-aov",
        "children",
    ),

    Output(
        "rt-revenue-sparkline",
        "figure",
    ),

    Output(
        "rt-order-feed",
        "children",
    ),

    Output(
        "rt-last-update",
        "children",
    ),

    Output(
        "rt-activity-chart",
        "figure",
    ),

    Input(
        "realtime-refresh",
        "n_intervals",
    ),
)
def update_realtime_dashboard(
    n_intervals,
):

    # --------------------------------------------------------
    # FETCH API DATA
    # --------------------------------------------------------

    today = get_api_data(
        "/analytics/today"
    )

    recent = get_api_data(
        "/analytics/recent"
    )


    # --------------------------------------------------------
    # NORMALIZE RECENT ORDERS
    # --------------------------------------------------------

    recent_rows = extract_rows(
        recent,
        [
            "orders",
            "data",
            "results",
            "recent_orders",
        ],
    )


    # --------------------------------------------------------
    # TODAY METRICS
    # --------------------------------------------------------

    today_orders = safe_int(
        first_value(
            today,
            [
                "orders",
                "total_orders",
                "today_orders",
                "order_count",
            ],
            0,
        )
    )

    today_revenue = safe_float(
        first_value(
            today,
            [
                "revenue",
                "total_revenue",
                "today_revenue",
                "sales",
            ],
            0,
        )
    )

    today_items = safe_int(
        first_value(
            today,
            [
                "items",
                "total_items",
                "today_items",
                "items_sold",
            ],
            0,
        )
    )


    # --------------------------------------------------------
    # FALLBACK FROM RECENT DATA
    # --------------------------------------------------------

    if (
        today_orders == 0
        and recent_rows
    ):

        today_orders = len(
            recent_rows
        )


    if (
        today_revenue == 0
        and recent_rows
    ):

        today_revenue = sum(
            get_order_amount(row)
            for row in recent_rows
        )


    if (
        today_items == 0
        and recent_rows
    ):

        today_items = sum(
            get_order_items(row)
            for row in recent_rows
        )


    # --------------------------------------------------------
    # AOV
    # --------------------------------------------------------

    api_aov = safe_float(
        first_value(
            today,
            [
                "aov",
                "average_order_value",
                "avg_order_value",
            ],
            0,
        )
    )

    if api_aov > 0:

        aov = api_aov

    elif today_orders > 0:

        aov = (
            today_revenue
            / today_orders
        )

    else:

        aov = 0


    # --------------------------------------------------------
    # SPARKLINE
    # --------------------------------------------------------

    sparkline = (
        create_revenue_sparkline(
            recent_rows
        )
    )


    # --------------------------------------------------------
    # ORDER FEED
    # --------------------------------------------------------

    order_feed = build_order_feed(
        recent_rows
    )


    # --------------------------------------------------------
    # UPDATE STATUS
    # --------------------------------------------------------

    if (
        today is None
        and recent is None
    ):

        last_update = (
            "FastAPI unavailable"
        )

    elif today is None:

        last_update = (
            "Partial data · "
            "FastAPI metrics unavailable"
        )

    else:

        last_update = (
            "● Live · Updated just now"
        )

    activity_chart = create_recent_activity_chart(recent_rows)


    # --------------------------------------------------------
    # RETURN ALL 8 OUTPUTS
    # --------------------------------------------------------

    return (
        f"R${today_revenue:,.2f}",
        f"{today_orders:,}",
        f"{today_items:,}",
        f"R${aov:,.2f}",
        sparkline,
        order_feed,
        last_update,
        activity_chart,
    )
