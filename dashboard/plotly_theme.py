import plotly.io as pio


# ============================================================
# PULSeCOMMERCE ANALYTICS
# GLOBAL PLOTLY THEME
# ============================================================

FONT_FAMILY = (
    "Inter, "
    "Manrope, "
    "Plus Jakarta Sans, "
    "Segoe UI, "
    "Arial, "
    "sans-serif"
)


ANALYTICS_TEMPLATE = {
    "layout": {

        # ----------------------------------------------------
        # Background
        # ----------------------------------------------------

        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",


        # ----------------------------------------------------
        # Typography
        # ----------------------------------------------------

        "font": {
            "family": FONT_FAMILY,
            "color": "#dbe7f1",
            "size": 10,
        },


        # ----------------------------------------------------
        # Color palette
        # ----------------------------------------------------

        "colorway": [
            "#22d3ee",
            "#8b5cf6",
            "#ec4899",
            "#34d399",
            "#60a5fa",
            "#a78bfa",
            "#2dd4bf",
            "#f472b6",
            "#f59e0b",
        ],


        # ----------------------------------------------------
        # Titles
        # ----------------------------------------------------

        "title": {
            "font": {
                "family": FONT_FAMILY,
                "size": 13,
                "color": "#edf4fb",
            },

            "x": 0.02,
            "xanchor": "left",

            "y": 0.98,
            "yanchor": "top",
        },


        # ----------------------------------------------------
        # Hover labels
        # ----------------------------------------------------

        "hoverlabel": {
            "bgcolor": "#0b1422",
            "bordercolor": "rgba(103,232,249,0.28)",

            "font": {
                "family": FONT_FAMILY,
                "color": "#f8fafc",
                "size": 10,
            },
        },


        # ----------------------------------------------------
        # X Axis
        # ----------------------------------------------------

        "xaxis": {
            "showgrid": True,

            "gridcolor":
                "rgba(148,163,184,0.065)",

            "gridwidth": 1,

            "zeroline": False,

            "linecolor":
                "rgba(148,163,184,0.10)",

            "tickfont": {
                "color": "#8190a4",
                "size": 8,
            },

            "title": {
                "font": {
                    "color": "#8190a4",
                    "size": 8,
                },
            },

            "automargin": True,

            "fixedrange": False,
        },


        # ----------------------------------------------------
        # Y Axis
        # ----------------------------------------------------

        "yaxis": {
            "showgrid": True,

            "gridcolor":
                "rgba(148,163,184,0.065)",

            "gridwidth": 1,

            "zeroline": False,

            "linecolor":
                "rgba(148,163,184,0.10)",

            "tickfont": {
                "color": "#8190a4",
                "size": 8,
            },

            "title": {
                "font": {
                    "color": "#8190a4",
                    "size": 8,
                },
            },

            "automargin": True,

            "fixedrange": False,
        },


        # ----------------------------------------------------
        # Legend
        # ----------------------------------------------------

        "legend": {
            "font": {
                "color": "#aebdcd",
                "size": 8,
            },

            "bgcolor":
                "rgba(0,0,0,0)",

            "borderwidth": 0,
        },


        # ----------------------------------------------------
        # Default chart spacing
        # ----------------------------------------------------

        "margin": {
            "l": 48,
            "r": 20,
            "t": 35,
            "b": 42,
        },


        # ----------------------------------------------------
        # Hover behavior
        # ----------------------------------------------------

        "hovermode": "closest",


        # ----------------------------------------------------
        # Text collision
        # ----------------------------------------------------

        "uniformtext": {
            "minsize": 8,
            "mode": "hide",
        },


        # ----------------------------------------------------
        # Responsive
        # ----------------------------------------------------

        "autosize": True,


        # ----------------------------------------------------
        # Annotation defaults
        # ----------------------------------------------------

        "annotationdefaults": {
            "font": {
                "family": FONT_FAMILY,
                "color": "#cbd5e1",
                "size": 9,
            },

            "arrowcolor": "#22d3ee",

            "arrowhead": 2,
        },
    }
}


# ============================================================
# REGISTER TEMPLATE
# ============================================================

pio.templates["analytics_dark"] = ANALYTICS_TEMPLATE