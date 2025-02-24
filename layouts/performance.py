import dash_bootstrap_components as dbc
from dash import html, dcc
from components.navbar import create_navbar
from utils.data_processing import DataProcessor

dp = DataProcessor()

# Obtener valores mínimos y máximos de partido
min_partido = 1
max_partido = 6  # Ajusta esto según tus datos

layout = html.Div([
    create_navbar(),
    dbc.Container([
        # Título principal
        dbc.Row([
            dbc.Col([
                html.H2("Dashboard de Performance", className="text-center mb-4"),
                html.P("Análisis de rendimiento individual y comparativo", 
                       className="text-center text-muted mb-4")
            ])
        ]),
        
        # SECCIÓN 1: ANÁLISIS INDIVIDUAL
        dbc.Card([
            dbc.CardHeader(html.H4("Análisis Individual", className="text-center")),
            dbc.CardBody([
                # Selector de jugador y filtros
                dbc.Row([
                    dbc.Col([
                        html.H5("Seleccionar Jugador"),
                        dcc.Dropdown(
                            id='player-selector',
                            options=[{'label': p, 'value': p} for p in dp.get_player_list()],
                            placeholder="Selecciona un jugador",
                            className="mb-4"
                        ),
                    ], md=6),
                    dbc.Col([
                        html.H5("Rango de Partidos"),
                        dcc.RangeSlider(
                            id='partido-range',
                            min=min_partido,
                            max=max_partido,
                            step=1,
                            marks={i: str(i) for i in range(min_partido, max_partido+1)},
                            value=[min_partido, max_partido],
                            className="mb-4"
                        ),
                    ], md=6),
                ]),

                # Estado de carga
                dbc.Spinner(
                    id="loading-1",
                    type="grow",
                    color="primary",
                    children=[html.Div(id="loading-output-1")]
                ),

                # Estadísticas principales
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3(id='total-goals', className="text-center"),
                                html.P("Goles", className="text-center text-muted")
                            ])
                        ])
                    ], md=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3(id='total-assists', className="text-center"),
                                html.P("Asistencias", className="text-center text-muted")
                            ])
                        ])
                    ], md=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3(id='pases-completados', className="text-center"),
                                html.P("Pases Completados", className="text-center text-muted")
                            ])
                        ])
                    ], md=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3(id='pases-fallados', className="text-center"),
                                html.P("Pases Fallados", className="text-center text-muted")
                            ])
                        ])
                    ], md=3)
                ], className="mb-4"),

                # Gráficos individuales
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='goals-chart')
                            ])
                        ])
                    ], md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='passes-chart')
                            ])
                        ])
                    ], md=6)
                ], className="mb-4"),

                # Gráfico de radar individual
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(
                                    id='radar-chart-1',
                                    style={'height': '600px'}
                                )
                            ])
                        ])
                    ])
                ]),

                # Botón de exportar PDF
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            "Exportar Reporte PDF",
                            id="export-pdf",
                            color="success",
                            className="mt-4"
                        ),
                        html.Div(id="export-status", className="mt-2")
                    ], className="text-center")
                ])
            ])
        ], className="mb-5"),

        # SECCIÓN 2: COMPARACIÓN
        dbc.Card([
            dbc.CardHeader(html.H4("Comparación de Jugadores", className="text-center")),
            dbc.CardBody([
                # Selector para comparación
                dbc.Row([
                    dbc.Col([
                        html.H5("Seleccionar Jugador para Comparar"),
                        dcc.Dropdown(
                            id='player2-selector',
                            options=[{'label': p, 'value': p} for p in dp.get_player_list()],
                            placeholder="Selecciona jugador para comparar",
                            className="mb-4"
                        ),
                    ])
                ]),

                # Estado de carga para comparación
                dbc.Spinner(
                    id="loading-2",
                    type="grow",
                    color="primary",
                    children=[html.Div(id="loading-output-2")]
                ),

                # Gráficos comparativos
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(
                                    id='radar-chart-2',
                                    style={'height': '600px'}
                                )
                            ])
                        ])
                    ], md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(
                                    id='comparison-stats',
                                    style={'height': '600px'}
                                )
                            ])
                        ])
                    ], md=6)
                ])
            ])
        ])
    ], className="py-4")
])