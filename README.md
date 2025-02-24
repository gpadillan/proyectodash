Dashboard Deportivo 
Dashboard interactivo para análisis y visualización de datos deportivos del Valencia CF, creado con Dash y Plotly.
Características

Sistema de autenticación para proteger el acceso a los datos
Dashboard de Performance con estadísticas detalladas y comparativas de jugadores
Dashboard Médico para seguimiento de lesiones y estado de los jugadores
Visualizaciones interactivas que permiten filtrar por partido y jugador
Exportación a PDF de informes de rendimiento
Diseño responsivo adaptado a la identidad visual del Valencia CF

Capturas de pantalla

Login: Sistema de autenticación seguro
Home: Página de bienvenida con acceso a las diferentes secciones
Performance: Análisis detallado de estadísticas individuales y comparativas
Área Médica: Seguimiento de lesiones y disponibilidad de jugadores
Credenciales

Usuario: admin
Contraseña: admin
Estructura del proyecto
sports_dashboard/
│
├── assets/
│   ├── custom.css
│   └── images/
│       └── valencia.png
│
├── data/
│   └── jugadores.csv
│
├── layouts/
│   ├── __init__.py
│   ├── home.py
│   ├── performance.py
│   └── medical.py
│
├── components/
│   ├── __init__.py
│   └── navbar.py
│
├── utils/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── cache.py
│   └── pdf_generator.py
│
├── app.py
├── requirements.txt
└── README.md


Funcionalidades implementadas
Dashboard de Performance

Visualización de goles, asistencias y pases por partido
Gráfico radar de habilidades del jugador (táctico, técnico, físico, conducta)
Comparación directa entre dos jugadores
Filtrado por rango de partidos
Exportación de informes en formato PDF

Dashboard Médico

Estadísticas de jugadores lesionados vs disponibles
Tiempo medio de baja por posición
Distribución de lesiones por tipo de jugador
Tecnologías utilizadas

Dash: Framework para aplicaciones web analíticas
Plotly: Biblioteca para gráficos interactivos
Flask-Login: Gestión de autenticación
Pandas: Procesamiento y análisis de datos
Bootstrap: Diseño responsivo
PDFKit: Generación de reportes PDF
