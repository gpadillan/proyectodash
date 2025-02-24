import dash_bootstrap_components as dbc
from dash import html
from components.navbar import create_navbar

layout = html.Div([
    create_navbar(),
    dbc.Container([
        # Header Section con Logo
        dbc.Row([
            dbc.Col([
                html.Div([
                    # Añadir el logo
                    html.Img(
                        src="/assets/images/valencia.png",
                        style={
                            'height': '150px',  # Ajusta estos valores según necesites
                            'margin-bottom': '20px'
                        }
                    ),
                    html.H1("Dashboard Deportivo Jugadores", 
                           className="display-4 text-center mb-3"),
                    html.P("Sistema de Análisis y Gestión de Rendimiento Deportivo",
                           className="lead text-center text-muted mb-4"),
                    html.Hr(className="my-4")
                ], className="text-center")
            ])
        ], className="mb-5"),
        # ... resto del código ...
    ])
])
