import dash_bootstrap_components as dbc
from dash import html, dcc
from components.navbar import create_navbar
from utils.data_processing import DataProcessor

dp = DataProcessor()

layout = html.Div([
    create_navbar(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Dashboard Médico", className="text-center mb-4"),
                html.P("Estado médico y lesiones del equipo", 
                       className="text-center text-muted mb-4")
            ])
        ]),
        
        # Tarjetas de resumen
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(id="total-injured", className="text-danger text-center"),
                        html.P("Jugadores Lesionados", className="text-center")
                    ])
                ])
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(id="avg-recovery-time", className="text-warning text-center"),
                        html.P("Días Promedio de Recuperación", className="text-center")
                    ])
                ])
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(id="players-available", className="text-success text-center"),
                        html.P("Jugadores Disponibles", className="text-center")
                    ])
                ])
            ], md=4),
        ], className="mb-4"),
        
        # Gráfico médico
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Estado Médico por Posición")),
                    dbc.CardBody([
                        dcc.Graph(id='medical-chart')
                    ])
                ])
            ])
        ], className="mb-4")
    ])
])
