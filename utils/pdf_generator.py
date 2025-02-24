import pdfkit
import pandas as pd
from datetime import datetime
import plotly.io as pio
import os

class PDFGenerator:
    def __init__(self, data_processor):
        self.dp = data_processor
        self.options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'no-outline': None
        }

    def generate_performance_report(self, player_name, min_partido=None, max_partido=None):
        """Genera un reporte PDF de rendimiento para un jugador específico"""
        
        # Crear directorio temporal si no existe
        if not os.path.exists('temp'):
            os.makedirs('temp')
            
        # Obtener estadísticas del jugador
        stats = self.dp.get_performance_stats(player_name, min_partido, max_partido)
        
        # Generar gráficos
        goals_fig = self.dp.create_goals_chart(player_name, min_partido, max_partido)
        passes_fig = self.dp.create_passes_chart(player_name, min_partido, max_partido)
        radar_fig = self.dp.create_radar_chart(player_name)
        
        # Guardar gráficos como imágenes temporales
        goals_fig.write_image("temp/goals.png")
        passes_fig.write_image("temp/passes.png")
        radar_fig.write_image("temp/radar.png")
        
        # Crear HTML del reporte
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ 
                        background-color: #343a40;
                        color: white;
                        padding: 20px;
                        text-align: center;
                    }}
                    .content {{ padding: 20px; }}
                    .stats-container {{
                        display: flex;
                        justify-content: space-between;
                        margin: 20px 0;
                    }}
                    .stat-box {{
                        background-color: #f5f5f5;
                        padding: 15px;
                        border-radius: 5px;
                        text-align: center;
                    }}
                    .chart-container {{
                        margin: 20px 0;
                        text-align: center;
                    }}
                    .logo {{
                        height: 50px;
                        margin-bottom: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <img src="assets/images/valencia.png" class="logo">
                    <h1>Reporte de Rendimiento</h1>
                    <p>{player_name} - {datetime.now().strftime('%d/%m/%Y')}</p>
                </div>
                
                <div class="content">
                    <div class="stats-container">
                        <div class="stat-box">
                            <h3>Goles Totales</h3>
                            <p>{stats['total_goals']}</p>
                        </div>
                        <div class="stat-box">
                            <h3>Asistencias</h3>
                            <p>{stats['total_assists']}</p>
                        </div>
                        <div class="stat-box">
                            <h3>Pases Completados</h3>
                            <p>{stats['pases_completados']}</p>
                        </div>
                    </div>
                    
                    <div class="chart-container">
                        <h2>Goles por Partido</h2>
                        <img src="temp/goals.png" style="max-width: 100%;">
                    </div>
                    
                    <div class="chart-container">
                        <h2>Análisis de Pases</h2>
                        <img src="temp/passes.png" style="max-width: 100%;">
                    </div>
                    
                    <div class="chart-container">
                        <h2>Perfil del Jugador</h2>
                        <img src="temp/radar.png" style="max-width: 100%;">
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Generar PDF
        output_path = f'reports/reporte_{player_name}_{datetime.now().strftime("%Y%m%d")}.pdf'
        if not os.path.exists('reports'):
            os.makedirs('reports')
            
        pdfkit.from_string(html_content, output_path, options=self.options)
        
        # Limpiar archivos temporales
        for temp_file in ['goals.png', 'passes.png', 'radar.png']:
            os.remove(f'temp/{temp_file}')
            
        return output_path