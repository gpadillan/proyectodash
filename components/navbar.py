import dash_bootstrap_components as dbc
from dash import html

def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Performance", href="/performance")),
            dbc.NavItem(dbc.NavLink("Medical", href="/medical")),
            dbc.NavItem(
                dbc.Button("Logout", id="logout-button", color="light", className="ml-2")
            ),
        ],
        brand=html.Div([
            html.Img(
                src="/assets/images/valencia.png",
                height="30px",
                className="me-2"
            ),
            "Valencia CF Dashboard"
        ], className="d-flex align-items-center"),
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4",
    )
    return navbar