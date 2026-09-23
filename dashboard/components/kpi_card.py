from dash import html


def create_kpi_card(
    title,
    value,
    icon="◆",
    variant="cyan",
    delta=None,
    delta_label=None,
    subtitle=None,
    sparkline=None,
):
    delta_component = None

    if delta is not None:
        arrow = "↑" if delta >= 0 else "↓"
        delta_class = (
            "kpi-delta-positive"
            if delta >= 0
            else "kpi-delta-negative"
        )

        label = delta_label or "MoM"

        delta_component = html.Span(
            f"{arrow} {abs(delta):.1f}% {label}",
            className=f"kpi-delta {delta_class}",
        )

    children = [
        html.Div(
            [
                html.Div(
                    icon,
                    className="kpi-icon",
                ),
                html.Div(
                    title,
                    className="kpi-label",
                ),
            ],
            className="kpi-card-top",
        ),

        html.Div(
            value,
            className="kpi-value",
        ),
    ]

    if delta_component is not None:
        children.append(
            html.Div(
                delta_component,
                className="kpi-meta",
            )
        )

    if subtitle:
        children.append(
            html.Div(
                subtitle,
                className="kpi-subtitle",
            )
        )

    if sparkline is not None:
        children.append(
            html.Div(
                sparkline,
                className="kpi-sparkline",
            )
        )

    return html.Div(
        children,
        className=f"kpi-card kpi-card-{variant}",
    )