from dash import html


def create_section_header(
    title,
    subtitle=None,
    action=None,
):
    children = [
        html.Div(
            [
                html.H2(
                    title,
                    className="section-title",
                ),

                html.Div(
                    subtitle,
                    className="section-subtitle",
                ) if subtitle else None,
            ]
        )
    ]

    if action:
        children.append(
            action
        )

    return html.Div(
        children=children,
        className="section-header",
    )