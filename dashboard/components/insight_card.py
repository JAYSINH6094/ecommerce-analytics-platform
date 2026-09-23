from dash import html


def create_insight_card(
    label,
    title,
    description=None,
    icon="✦",
    variant="violet",
):
    children = [
        html.Div(
            icon,
            className=f"insight-icon insight-icon-{variant}",
        ),

        html.Div(
            [
                html.Div(
                    label,
                    className="insight-label",
                ),

                html.Div(
                    title,
                    className="insight-title",
                ),

                html.Div(
                    description,
                    className="insight-description",
                ) if description else None,
            ],
            className="insight-copy",
        ),
    ]

    return html.Div(
        children=children,
        className=f"insight-card insight-card-{variant}",
    )


def create_insight_item(
    title,
    description,
    icon="✦",
    variant="cyan",
):
    return html.Div(
        className=f"insight-item insight-item-{variant}",
        children=[
            html.Div(
                icon,
                className="insight-item-icon",
            ),

            html.Div(
                [
                    html.Div(
                        title,
                        className="insight-item-title",
                    ),
                    html.Div(
                        description,
                        className="insight-item-description",
                    ),
                ],
                className="insight-item-copy",
            ),
        ],
    )