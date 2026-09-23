from dash import dcc, html


def create_chart_card(
    title,
    figure,
    class_name="",
    subtitle=None,
    action=None,
    graph_id=None,
    height=None,
):
    """
    Reusable glass chart panel for PulseCommerce dashboards.
    """

    header_children = [
        html.Div(
            [
                html.Div(
                    title,
                    className="chart-card-title",
                ),
                (
                    html.Div(
                        subtitle,
                        className="chart-card-subtitle",
                    )
                    if subtitle
                    else None
                ),
            ],
            className="chart-card-heading",
        )
    ]

    if action is not None:
        header_children.append(
            html.Div(
                action,
                className="chart-card-action",
            )
        )

    graph_kwargs = {
        "figure": figure,
        "config": {
            "displayModeBar": False,
            "responsive": True,
        },
        "style": {
            "width": "100%",
            "height": (
                f"{height}px"
                if height is not None
                else "100%"
            ),
        },
    }

    # Dash does not accept id=None.
    # Only add the id when a real id was supplied.
    if graph_id is not None:
        graph_kwargs["id"] = graph_id

    return html.Div(
        [
            html.Div(
                header_children,
                className="chart-card-header",
            ),

            html.Div(
                dcc.Graph(**graph_kwargs),
                className="chart-card-body",
            ),
        ],
        className=f"chart-card {class_name}".strip(),
    )