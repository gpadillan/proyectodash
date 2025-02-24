import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.cache import cache_data_processing

class DataProcessor:
    def __init__(self):
        self.df = pd.read_csv('data/jugadores.csv')
        
    @cache_data_processing
    def get_player_list(self):
        """Obtener lista de jugadores únicos"""
        return sorted(self.df['Nombre'].unique())
    
    @cache_data_processing
    def get_performance_stats(self, player_name=None, min_partido=None, max_partido=None):
        """Obtener estadísticas de rendimiento filtradas por partido"""
        data = self.df.copy()
        
        if player_name:
            data = data[data['Nombre'] == player_name]
        if min_partido is not None:
            data = data[data['Partido'] >= min_partido]
        if max_partido is not None:
            data = data[data['Partido'] <= max_partido]
            
        stats = {
            'total_goals': int(data['Goles Favor'].sum()),
            'total_assists': int(data['Asistencias'].sum()),
            'avg_minutes': float(data['Minutos Jugados'].mean()),
            'pases_completados': int(data['Pases Completados'].sum()),
            'pases_fallados': int(data['Pases Fallados'].sum()),
            'efectividad': round((data['Pases Completados'].sum() / 
                                (data['Pases Completados'].sum() + data['Pases Fallados'].sum())) * 100, 2) if (data['Pases Completados'].sum() + data['Pases Fallados'].sum()) > 0 else 0
        }
        return stats

    @cache_data_processing
    def create_goals_chart(self, player_name=None, min_partido=None, max_partido=None):
        """Crear gráfico de goles por partido mejorado"""
        data = self.df.copy()
        
        if player_name:
            data = data[data['Nombre'] == player_name]
        if min_partido is not None:
            data = data[data['Partido'] >= min_partido]
        if max_partido is not None:
            data = data[data['Partido'] <= max_partido]
            
        fig = go.Figure()
        
        # Añadir barras para goles
        fig.add_trace(go.Bar(
            x=data['Partido'],
            y=data['Goles Favor'],
            name='Goles',
            marker_color='#ff6b00',
            hovertemplate="Partido %{x}<br>Goles: %{y}<extra></extra>"
        ))
        
        # Añadir línea de promedio
        avg_goals = data['Goles Favor'].mean()
        fig.add_hline(y=avg_goals, 
                     line_dash="dash", 
                     line_color="#343a40",
                     annotation_text=f"Promedio: {avg_goals:.2f}")
        
        fig.update_layout(
            title=dict(
                text='Goles por Partido',
                x=0.5,
                y=0.95
            ),
            xaxis_title='Partido',
            yaxis_title='Goles',
            template='plotly_white',
            hovermode='x unified'
        )
        return fig

    @cache_data_processing
    def create_passes_chart(self, player_name=None, min_partido=None, max_partido=None):
        """Crear gráfico de pases por partido"""
        data = self.df.copy()
        
        if player_name:
            data = data[data['Nombre'] == player_name]
        if min_partido is not None:
            data = data[data['Partido'] >= min_partido]
        if max_partido is not None:
            data = data[data['Partido'] <= max_partido]
            
        fig = go.Figure()
        
        # Añadir barras para pases completados
        fig.add_trace(go.Bar(
            x=data['Partido'],
            y=data['Pases Completados'],
            name='Pases Completados',
            marker_color='#2ed573',
            hovertemplate="Partido %{x}<br>Pases Completados: %{y}<extra></extra>"
        ))
        
        # Añadir barras para pases fallados
        fig.add_trace(go.Bar(
            x=data['Partido'],
            y=data['Pases Fallados'],
            name='Pases Fallados',
            marker_color='#ff4757',
            hovertemplate="Partido %{x}<br>Pases Fallados: %{y}<extra></extra>"
        ))
        
        fig.update_layout(
            title=dict(
                text='Pases por Partido',
                x=0.5,
                y=0.95
            ),
            xaxis_title='Partido',
            yaxis_title='Número de Pases',
            barmode='group',
            template='plotly_white',
            hovermode='x unified'
        )
        return fig
    
    @cache_data_processing
    def create_radar_chart(self, player_name):
        """Crear gráfico de radar con habilidades del jugador"""
        player_data = self.df[self.df['Nombre'] == player_name].iloc[0]
        
        categories = ['Táctico', 'Técnico', 'Físico', 'Conducta']
        values = [player_data['Táctico'], player_data['Técnico'], 
                 player_data['Físico'], player_data['Conducta']]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=player_name,
            line=dict(color='#ff6b00')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    showline=True,
                    linewidth=1,
                    gridcolor='rgba(0,0,0,0.1)',
                    nticks=10
                ),
                angularaxis=dict(
                    showline=True,
                    linewidth=1,
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                bgcolor='white'
            ),
            showlegend=True,
            height=600,
            title=dict(
                text=f"Perfil de {player_name}",
                x=0.5,
                y=0.95
            )
        )
        return fig
    
    @cache_data_processing
    def create_performance_comparison(self, player1, player2):
        """Crear gráfico comparativo de dos jugadores"""
        data1 = self.df[self.df['Nombre'] == player1]
        data2 = self.df[self.df['Nombre'] == player2]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Goles por Partido', 'Minutos Jugados',
                          'Pases Completados', 'Asistencias')
        )
        
        # Goles
        fig.add_trace(
            go.Scatter(x=data1['Partido'], y=data1['Goles Favor'],
                      name=f'{player1} - Goles',
                      line=dict(color='#ff6b00')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=data2['Partido'], y=data2['Goles Favor'],
                      name=f'{player2} - Goles',
                      line=dict(color='#343a40')),
            row=1, col=1
        )
        
        # Minutos
        fig.add_trace(
            go.Scatter(x=data1['Partido'], y=data1['Minutos Jugados'],
                      name=f'{player1} - Minutos',
                      line=dict(color='#ff6b00')),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=data2['Partido'], y=data2['Minutos Jugados'],
                      name=f'{player2} - Minutos',
                      line=dict(color='#343a40')),
            row=1, col=2
        )
        
        # Pases
        fig.add_trace(
            go.Bar(x=data1['Partido'], y=data1['Pases Completados'],
                  name=f'{player1} - Pases',
                  marker_color='#ff6b00'),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=data2['Partido'], y=data2['Pases Completados'],
                  name=f'{player2} - Pases',
                  marker_color='#343a40'),
            row=2, col=1
        )
        
        # Asistencias
        fig.add_trace(
            go.Bar(x=data1['Partido'], y=data1['Asistencias'],
                  name=f'{player1} - Asistencias',
                  marker_color='#ff6b00'),
            row=2, col=2
        )
        fig.add_trace(
            go.Bar(x=data2['Partido'], y=data2['Asistencias'],
                  name=f'{player2} - Asistencias',
                  marker_color='#343a40'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Comparación de Rendimiento",
            template='plotly_white'
        )
        
        return fig

    def create_medical_chart(self):
        """Crear gráfico para el dashboard médico"""
        medical_stats = self.df.groupby('Posición').agg({
            'Lesionado': 'sum',
            'Tiempo Baja': 'mean',
            'Estado Actual': lambda x: (x == 'Disponible').sum()
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Lesionados',
            x=medical_stats['Posición'],
            y=medical_stats['Lesionado'],
            marker_color='#ff4757'
        ))
        
        fig.add_trace(go.Bar(
            name='Disponibles',
            x=medical_stats['Posición'],
            y=medical_stats['Estado Actual'],
            marker_color='#2ed573'
        ))
        
        fig.update_layout(
            title='Estado Médico por Posición',
            barmode='group',
            template='plotly_white',
            height=500
        )
        
        return fig