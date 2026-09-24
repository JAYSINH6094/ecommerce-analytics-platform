from dash import html, dcc


def create_sidebar():
    return html.Aside(
        className="app-sidebar",
        children=[
            # ------------------------------------------------
            # BRAND
            # ------------------------------------------------

            html.Div(
                className="brand",
                children=[
                    html.Img(
                        src="/assets/favicon.svg",
                        className="brand-mark",
                        alt="PulseCommerce",
                    ),

                    html.Div(
                        [
                            html.Div(
                                "PulseCommerce",
                                className="brand-name",
                            ),
                            html.Div(
                                "Analytics Platform",
                                className="brand-subtitle",
                            ),
                        ],
                        className="brand-copy",
                    ),
                ],
            ),

            html.Div(
                className="sidebar-divider"
            ),

            # ------------------------------------------------
            # NAVIGATION
            # ------------------------------------------------

            html.Nav(
                className="sidebar-nav",
                children=[
                    dcc.Link(
                        [
                            html.Span(
                                "⌂",
                                className="sidebar-link-icon",
                            ),
                            html.Span(
                                "Executive",
                                className="sidebar-link-label",
                            ),
                        ],
                        href="/",
                        id="nav-executive",
                        className="sidebar-link",
                    ),

                    dcc.Link(
                        [
                            html.Span(
                                "◉",
                                className="sidebar-link-icon",
                            ),
                            html.Span(
                                "Customers",
                                className="sidebar-link-label",
                            ),
                        ],
                        href="/customers",
                        id="nav-customers",
                        className="sidebar-link",
                    ),

                    dcc.Link(
                        [
                            html.Span(
                                "◇",
                                className="sidebar-link-icon",
                            ),
                            html.Span(
                                "Products",
                                className="sidebar-link-label",
                            ),
                        ],
                        href="/products",
                        id="nav-products",
                        className="sidebar-link",
                    ),

                    dcc.Link(
                        [
                            html.Span(
                                "◎",
                                className="sidebar-link-icon",
                            ),
                            html.Span(
                                "Regional",
                                className="sidebar-link-label",
                            ),
                        ],
                        href="/regional",
                        id="nav-regional",
                        className="sidebar-link",
                    ),

                    dcc.Link(
                        [
                            html.Span(
                                "◌",
                                className="sidebar-link-icon",
                            ),
                            html.Span(
                                "Real-Time",
                                className="sidebar-link-label",
                            ),
                            html.Span(
                                "LIVE",
                                className="sidebar-live",
                            ),
                        ],
                        href="/realtime",
                        id="nav-realtime",
                        className="sidebar-link",
                    ),
                ],
            ),
        ],
    )