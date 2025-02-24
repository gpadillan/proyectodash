import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import plotly.express as px
import plotly.graph_objects as go
from layouts import home, performance, medical
from utils.data_processing import DataProcessor
from utils.pdf_generator import PDFGenerator
import os

# Inicializar la aplicación
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)

server = app.server
server.config.update(SECRET_KEY='tu_clave_secreta_123')
app.title = "Valencia CF Dashboard"

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)

# Clase simple de Usuario
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    return User(username)

# Layout de login
login_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Img(
                        src="/assets/images/valencia.png",
                        height="100px",
                        className="mb-3"
                    ),
                    html.H4("Login", className="text-center")
                ], className="text-center"),
                dbc.CardBody([
                    dbc.Input(
                        id="username-input",
                        placeholder="Usuario",
                        type="text",
                        className="mb-3"
                    ),
                    dbc.Input(
                        id="password-input",
                        placeholder="Contraseña",
                        type="password",
                        className="mb-3"
                    ),
                    dbc.Button(
                        "Iniciar Sesión",
                        id="login-button",
                        color="primary",
                        className="w-100"
                    ),
                    html.Div(id="login-error")
                ])
            ])
        ], width=6, className="mx-auto")
    ], className="vh-100 align-items-center")
])

# Layout principal
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback para manejo de páginas
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/login' or not current_user.is_authenticated:
        return login_layout
    elif pathname == '/':
        return home.layout
    elif pathname == '/performance':
        return performance.layout
    elif pathname == '/medical':
        return medical.layout
    else:
        return home.layout

# Callback para el login
@app.callback(
    [dash.dependencies.Output('login-error', 'children'),
     dash.dependencies.Output('url', 'pathname')],
    [dash.dependencies.Input('login-button', 'n_clicks')],
    [dash.dependencies.State('username-input', 'value'),
     dash.dependencies.State('password-input', 'value')]
)
def login_callback(n_clicks, username, password):
    if n_clicks is None:
        return '', '/login'
    if username == 'admin' and password == 'admin':
        user = User(username)
        login_user(user)
        return '', '/'
    return 'Usuario o contraseña incorrectos', '/login'

# Callback para el dashboard de performance
@app.callback(
    [
        dash.dependencies.Output('total-goals', 'children'),
        dash.dependencies.Output('total-assists', 'children'),
        dash.dependencies.Output('pases-completados', 'children'),
        dash.dependencies.Output('pases-fallados', 'children'),
        dash.dependencies.Output('goals-chart', 'figure'),
        dash.dependencies.Output('passes-chart', 'figure'),
        dash.dependencies.Output('radar-chart-1', 'figure'),
        dash.dependencies.Output('loading-output-1', 'children')
    ],
    [
        dash.dependencies.Input('player-selector', 'value'),
        dash.dependencies.Input('partido-range', 'value')
    ]
)
def update_performance_dashboard(selected_player, partido_range):
    try:
        dp = DataProcessor()
        
        if not selected_player:
            empty_fig = px.scatter(title="Selecciona un jugador")
            return "0", "0", "0", "0", empty_fig, empty_fig, empty_fig, ""
        
        # Obtener valores de rango
        min_partido, max_partido = partido_range if partido_range else (None, None)
        
        # Obtener estadísticas
        stats = dp.get_performance_stats(selected_player, min_partido, max_partido)
        goals_fig = dp.create_goals_chart(selected_player, min_partido, max_partido)
        passes_fig = dp.create_passes_chart(selected_player, min_partido, max_partido)
        radar_fig = dp.create_radar_chart(selected_player)
        
        return (
            f"{stats['total_goals']}",
            f"{stats['total_assists']}",
            f"{stats['pases_completados']}",
            f"{stats['pases_fallados']}",
            goals_fig,
            passes_fig,
            radar_fig,
            ""
        )
    except Exception as e:
        print("Error en el callback:", e)
        empty_fig = px.scatter(title="Error al cargar datos")
        return "Error", "Error", "Error", "Error", empty_fig, empty_fig, empty_fig, ""

# Callback para la comparación
@app.callback(
    [
        dash.dependencies.Output('radar-chart-2', 'figure'),
        dash.dependencies.Output('comparison-stats', 'figure'),
        dash.dependencies.Output('loading-output-2', 'children')
    ],
    [
        dash.dependencies.Input('player-selector', 'value'),
        dash.dependencies.Input('player2-selector', 'value')
    ]
)
def update_comparison(player1, player2):
    try:
        dp = DataProcessor()
        
        if not player1 or not player2:
            empty_fig = px.scatter(title="Selecciona dos jugadores para comparar")
            return empty_fig, empty_fig, ""
            
        radar2 = dp.create_radar_chart(player2)
        comparison_fig = dp.create_performance_comparison(player1, player2)
        
        return radar2, comparison_fig, ""
    except Exception as e:
        print("Error en la comparación:", e)
        empty_fig = px.scatter(title="Error al cargar comparación")
        return empty_fig, empty_fig, ""

# Callback para exportar PDF
@app.callback(
    dash.dependencies.Output('export-status', 'children'),
    [dash.dependencies.Input('export-pdf', 'n_clicks')],
    [dash.dependencies.State('player-selector', 'value'),
     dash.dependencies.State('partido-range', 'value')]
)
def export_to_pdf(n_clicks, player, partido_range):
    if n_clicks is None or not player:
        return ""
    
    try:
        dp = DataProcessor()
        pdf_gen = PDFGenerator(dp)
        
        # Obtener valores de rango
        min_partido, max_partido = partido_range if partido_range else (None, None)
        
        # Generar PDF
        pdf_path = pdf_gen.generate_performance_report(player, min_partido, max_partido)
        
        return html.Div([
            html.P("PDF generado exitosamente!", className="text-success"),
            html.A("Descargar PDF", href=f"/{pdf_path}", className="btn btn-primary mt-2")
        ])
    except Exception as e:
        print("Error al generar PDF:", e)
        return html.P("Error al generar PDF", className="text-danger")

# Callback para el dashboard médico
@app.callback(
    [
        dash.dependencies.Output('total-injured', 'children'),
        dash.dependencies.Output('avg-recovery-time', 'children'),
        dash.dependencies.Output('players-available', 'children'),
        dash.dependencies.Output('medical-chart', 'figure')
    ],
    [dash.dependencies.Input('url', 'pathname')]
)
def update_medical_dashboard(pathname):
    if pathname != '/medical':
        return "0", "0", "0", {}
    
    try:
        dp = DataProcessor()
        total_injured = len(dp.df[dp.df['Lesionado'] == True])
        avg_recovery = dp.df[dp.df['Tiempo Baja'] > 0]['Tiempo Baja'].mean()
        available_players = len(dp.df[dp.df['Estado Actual'] == 'Disponible'])
        
        medical_chart = dp.create_medical_chart()
        
        return (
            str(total_injured),
            f"{avg_recovery:.1f}",
            str(available_players),
            medical_chart
        )
    except Exception as e:
        print("Error en medical dashboard:", e)
        return "Error", "Error", "Error", {}

if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs('reports', exist_ok=True)
    os.makedirs('temp', exist_ok=True)
    
    app.run_server(debug=True)
    