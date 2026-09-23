from dash import Dash, html, page_container

from dashboard import plotly_theme
from dashboard.components.sidebar import create_sidebar


app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
)

app.title = "PulseCommerce Analytics"



# ============================================================
# APPLICATION
# ============================================================

app.layout = html.Div(
    className="app-shell",
    children=[
        create_sidebar(),

        html.Main(
            className="app-main",
            children=[
                html.Div(
                    className="page-content",
                    children=page_container,
                ),
            ],
        ),
    ],
)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        dev_tools_ui=False,
    )