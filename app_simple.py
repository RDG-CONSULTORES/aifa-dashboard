#!/usr/bin/env python3
"""
AIFA Dashboard - Simplified Demo Version
Executive Dashboard for Felipe Ángeles International Airport
"""

import dash
from dash import Dash, html, dcc, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Initialize Dash app
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Simulated data
def get_kpi_data():
    return {
        'participation_passengers': {'current': 12.8, 'change': 2.3, 'target': 15.0},
        'participation_operations': {'current': 9.7, 'change': 1.8, 'target': 12.0},
        'participation_cargo': {'current': 8.4, 'change': 3.1, 'target': 10.0},
        'growth_vs_market': {'current': 5.5, 'change': 0.8},
        'punctuality': {'current': 87.2, 'change': -1.3, 'target': 90.0},
        'route_utilization': {'current': 78.4, 'change': 2.1, 'target': 85.0}
    }

def get_historical_data():
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
              'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    passengers = [8.2, 8.6, 9.1, 9.5, 10.2, 10.8, 11.3, 11.7, 12.1, 12.4, 12.6, 12.8]
    operations = [6.8, 7.1, 7.5, 7.9, 8.3, 8.7, 9.0, 9.3, 9.5, 9.6, 9.7, 9.7]
    return {'months': months, 'passengers': passengers, 'operations': operations}

def get_route_data():
    return [
        {'city': 'Los Angeles', 'passengers': 87000, 'load_factor': 85.7},
        {'city': 'Houston', 'passengers': 76000, 'load_factor': 81.3},
        {'city': 'Miami', 'passengers': 92000, 'load_factor': 87.4},
        {'city': 'Guadalajara', 'passengers': 125000, 'load_factor': 82.3},
        {'city': 'Monterrey', 'passengers': 98000, 'load_factor': 78.5},
        {'city': 'Cancún', 'passengers': 156000, 'load_factor': 89.2}
    ]

def get_airport_comparison():
    return [
        {'name': 'AICM', 'passengers': 48.2, 'change': -2.1},
        {'name': 'AIFA', 'passengers': 12.8, 'change': 2.3},
        {'name': 'Guadalajara', 'passengers': 8.9, 'change': 0.8},
        {'name': 'Cancún', 'passengers': 15.4, 'change': 1.2},
        {'name': 'Monterrey', 'passengers': 7.2, 'change': -0.3},
        {'name': 'Tijuana', 'passengers': 4.9, 'change': 0.5}
    ]

# Create KPI card component
def create_kpi_card(title, value, change, icon="📊", target=None):
    trend_color = '#00ff88' if change > 0 else '#ff4757'
    trend_arrow = '↗' if change > 0 else '↘'
    
    progress = (value / target * 100) if target else None
    
    return html.Div([
        html.Div([
            html.Div([
                html.Span(icon, style={'fontSize': '24px', 'color': '#00d4ff'})
            ], style={'marginRight': '15px'}),
            html.Div([
                html.H6(title, style={'color': '#8b92a9', 'margin': '0', 'fontSize': '12px'}),
                html.H3(f"{value}%", style={'color': 'white', 'margin': '5px 0', 'fontSize': '28px'}),
                html.Div([
                    html.Span(trend_arrow, style={'color': trend_color, 'fontSize': '16px'}),
                    html.Span(f"{change:+.1f}%", style={'color': trend_color, 'marginLeft': '5px'})
                ]),
                html.Small("vs mes anterior", style={'color': '#8b92a9', 'fontSize': '10px'})
            ])
        ], style={'display': 'flex', 'alignItems': 'center'}),
        
        # Progress bar if target exists
        html.Div([
            html.Div(style={
                'width': f"{progress if progress else 0}%",
                'height': '4px',
                'background': 'linear-gradient(90deg, #00d4ff, #f59e0b)',
                'borderRadius': '2px',
                'marginTop': '10px'
            }) if target else None,
            html.Small(f"Meta: {target}%" if target else "", 
                      style={'color': '#8b92a9', 'fontSize': '10px'})
        ]) if target else None
    ], style={
        'background': 'rgba(255, 255, 255, 0.05)',
        'backdropFilter': 'blur(20px)',
        'border': '1px solid rgba(0, 212, 255, 0.2)',
        'borderRadius': '16px',
        'padding': '20px',
        'margin': '10px',
        'boxShadow': '0 8px 32px rgba(0, 0, 0, 0.3)',
        'transition': 'transform 0.3s ease',
        'cursor': 'pointer'
    })

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.Div([
                html.Span("✈️", style={'fontSize': '32px', 'marginRight': '15px'}),
                html.Div([
                    html.H1("Centro de Operaciones AIFA", style={
                        'background': 'linear-gradient(90deg, #00d4ff, #f59e0b)',
                        'WebkitBackgroundClip': 'text',
                        'WebkitTextFillColor': 'transparent',
                        'fontSize': '28px',
                        'margin': '0'
                    }),
                    html.P("Aeropuerto Internacional Felipe Ángeles", 
                          style={'color': '#8b92a9', 'margin': '0', 'fontSize': '14px'})
                ])
            ], style={'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                html.Small("Última actualización: ", style={'color': '#8b92a9'}),
                html.Span(id="live-update-time", style={'color': '#00d4ff', 'fontWeight': '600'})
            ])
        ], style={
            'display': 'flex', 
            'justifyContent': 'space-between', 
            'alignItems': 'center',
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '0 20px'
        })
    ], style={
        'background': 'rgba(255, 255, 255, 0.05)',
        'backdropFilter': 'blur(20px)',
        'borderBottom': '1px solid rgba(0, 212, 255, 0.2)',
        'padding': '15px 0',
        'marginBottom': '20px'
    }),
    
    # Navigation tabs
    html.Div([
        dcc.Tabs(id="tabs", value="strategic", children=[
            dcc.Tab(label="KPIs Estratégicos", value="strategic"),
            dcc.Tab(label="Análisis Geográfico", value="geographic"),
            dcc.Tab(label="Análisis Financiero", value="financial"),
            dcc.Tab(label="Capacidad Operativa", value="capacity"),
            dcc.Tab(label="Seguridad", value="security"),
            dcc.Tab(label="Calidad de Servicio", value="quality"),
            dcc.Tab(label="Productividad", value="productivity")
        ], style={
            'background': 'rgba(255, 255, 255, 0.03)',
            'backdropFilter': 'blur(10px)',
            'border': '1px solid rgba(0, 212, 255, 0.2)',
            'borderRadius': '12px',
            'overflow': 'hidden'
        })
    ], style={'maxWidth': '1200px', 'margin': '0 auto 20px auto', 'padding': '0 20px'}),
    
    # Tab content
    html.Div(id="tab-content", style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '0 20px'}),
    
    # Auto-update interval
    dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0)
    
], style={
    'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    'background': 'linear-gradient(135deg, #0a0e27 0%, #1a1f37 50%, #0a0e27 100%)',
    'minHeight': '100vh',
    'color': 'white'
})

# Callback for tab content
@callback(Output("tab-content", "children"),
          Input("tabs", "value"))
def render_tab_content(active_tab):
    if active_tab == "strategic":
        return render_strategic_tab()
    elif active_tab == "geographic":
        return render_geographic_tab()
    elif active_tab == "financial":
        return render_financial_tab()
    else:
        return html.Div([
            html.H4(f"Módulo: {active_tab.title()}", style={'color': '#8b92a9', 'textAlign': 'center', 'marginTop': '50px'}),
            html.P("En desarrollo - Framework implementado", style={'color': '#8b92a9', 'textAlign': 'center'})
        ])

def render_strategic_tab():
    kpi_data = get_kpi_data()
    
    return html.Div([
        # KPI Cards Row 1
        html.Div([
            html.Div([
                create_kpi_card(
                    "Participación Nacional Pasajeros",
                    kpi_data['participation_passengers']['current'],
                    kpi_data['participation_passengers']['change'],
                    "👥",
                    kpi_data['participation_passengers']['target']
                )
            ], style={'flex': '1'}),
            html.Div([
                create_kpi_card(
                    "Participación Nacional Operaciones",
                    kpi_data['participation_operations']['current'],
                    kpi_data['participation_operations']['change'],
                    "✈️",
                    kpi_data['participation_operations']['target']
                )
            ], style={'flex': '1'}),
            html.Div([
                create_kpi_card(
                    "Participación Nacional Carga",
                    kpi_data['participation_cargo']['current'],
                    kpi_data['participation_cargo']['change'],
                    "📦",
                    kpi_data['participation_cargo']['target']
                )
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'gap': '10px', 'marginBottom': '20px'}),
        
        # KPI Cards Row 2
        html.Div([
            html.Div([
                create_kpi_card(
                    "Crecimiento vs Mercado",
                    kpi_data['growth_vs_market']['current'],
                    kpi_data['growth_vs_market']['change'],
                    "📈"
                )
            ], style={'flex': '1'}),
            html.Div([
                create_kpi_card(
                    "Puntualidad de Vuelos",
                    kpi_data['punctuality']['current'],
                    kpi_data['punctuality']['change'],
                    "⏰",
                    kpi_data['punctuality']['target']
                )
            ], style={'flex': '1'}),
            html.Div([
                create_kpi_card(
                    "Utilización de Rutas",
                    kpi_data['route_utilization']['current'],
                    kpi_data['route_utilization']['change'],
                    "🗺️",
                    kpi_data['route_utilization']['target']
                )
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'gap': '10px', 'marginBottom': '20px'}),
        
        # Charts Row
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Evolución Participación de Mercado", style={'color': 'white', 'margin': '0 0 5px 0'}),
                    html.Small("Últimos 12 meses", style={'color': '#8b92a9'})
                ], style={'padding': '15px 15px 0 15px'}),
                dcc.Graph(id="participation-trend-chart")
            ], style={
                'background': 'rgba(255, 255, 255, 0.05)',
                'backdropFilter': 'blur(20px)',
                'border': '1px solid rgba(0, 212, 255, 0.2)',
                'borderRadius': '16px',
                'marginRight': '10px',
                'flex': '2'
            }),
            html.Div([
                html.Div([
                    html.H5("Progreso Meta Anual", style={'color': 'white', 'margin': '0 0 5px 0'}),
                    html.Small("Participación de pasajeros", style={'color': '#8b92a9'})
                ], style={'padding': '15px 15px 0 15px'}),
                dcc.Graph(id="progress-gauge")
            ], style={
                'background': 'rgba(255, 255, 255, 0.05)',
                'backdropFilter': 'blur(20px)',
                'border': '1px solid rgba(0, 212, 255, 0.2)',
                'borderRadius': '16px',
                'flex': '1'
            })
        ], style={'display': 'flex', 'marginBottom': '20px'}),
        
        # Comparison Chart
        html.Div([
            html.Div([
                html.H5("Comparativo Aeropuertos Mexicanos", style={'color': 'white', 'margin': '0 0 5px 0'}),
                html.Small("Participación de mercado nacional", style={'color': '#8b92a9'})
            ], style={'padding': '15px 15px 0 15px'}),
            dcc.Graph(id="airport-comparison-chart")
        ], style={
            'background': 'rgba(255, 255, 255, 0.05)',
            'backdropFilter': 'blur(20px)',
            'border': '1px solid rgba(0, 212, 255, 0.2)',
            'borderRadius': '16px'
        })
    ])

def render_geographic_tab():
    route_data = get_route_data()
    
    return html.Div([
        html.H4("Análisis Geográfico", style={'color': 'white', 'marginBottom': '20px'}),
        
        # Top destinations
        html.Div([
            html.H5("Top Destinos AIFA", style={'color': 'white', 'marginBottom': '15px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Strong(route['city'], style={'color': 'white'}),
                        html.Br(),
                        html.Small(f"{route['passengers']:,} pasajeros", style={'color': '#8b92a9'}),
                        html.Br(),
                        html.Small(f"Factor de carga: {route['load_factor']}%", style={'color': '#00d4ff'})
                    ], style={'padding': '15px'})
                ], style={
                    'background': 'rgba(255, 255, 255, 0.03)',
                    'border': '1px solid rgba(255, 255, 255, 0.1)',
                    'borderRadius': '8px',
                    'margin': '5px',
                    'transition': 'all 0.3s ease',
                    'cursor': 'pointer'
                }) for route in route_data
            ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))', 'gap': '10px'})
        ], style={
            'background': 'rgba(255, 255, 255, 0.05)',
            'backdropFilter': 'blur(20px)',
            'border': '1px solid rgba(0, 212, 255, 0.2)',
            'borderRadius': '16px',
            'padding': '20px'
        })
    ])

def render_financial_tab():
    return html.Div([
        html.H4("Análisis Financiero", style={'color': 'white', 'marginBottom': '20px'}),
        
        html.Div([
            html.Div([
                html.H5("Ingresos Mensuales", style={'color': 'white', 'marginBottom': '10px'}),
                html.H3("$324.5M MXN", style={'color': '#00d4ff', 'margin': '0'}),
                html.Small("↗ +8.2% vs mes anterior", style={'color': '#00ff88'})
            ], style={
                'background': 'rgba(255, 255, 255, 0.05)',
                'backdropFilter': 'blur(20px)',
                'border': '1px solid rgba(0, 212, 255, 0.2)',
                'borderRadius': '16px',
                'padding': '20px',
                'margin': '10px',
                'flex': '1'
            }),
            html.Div([
                html.H5("Margen EBITDA", style={'color': 'white', 'marginBottom': '10px'}),
                html.H3("24.7%", style={'color': '#f59e0b', 'margin': '0'}),
                html.Small("↗ +1.3% vs mes anterior", style={'color': '#00ff88'})
            ], style={
                'background': 'rgba(255, 255, 255, 0.05)',
                'backdropFilter': 'blur(20px)',
                'border': '1px solid rgba(0, 212, 255, 0.2)',
                'borderRadius': '16px',
                'padding': '20px',
                'margin': '10px',
                'flex': '1'
            }),
            html.Div([
                html.H5("ROI Anual", style={'color': 'white', 'marginBottom': '10px'}),
                html.H3("18.4%", style={'color': '#00ff88', 'margin': '0'}),
                html.Small("↗ +2.1% vs año anterior", style={'color': '#00ff88'})
            ], style={
                'background': 'rgba(255, 255, 255, 0.05)',
                'backdropFilter': 'blur(20px)',
                'border': '1px solid rgba(0, 212, 255, 0.2)',
                'borderRadius': '16px',
                'padding': '20px',
                'margin': '10px',
                'flex': '1'
            })
        ], style={'display': 'flex', 'gap': '10px'})
    ])

# Callbacks for charts
@callback(Output('participation-trend-chart', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_participation_trend(n):
    data = get_historical_data()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['months'],
        y=data['passengers'],
        mode='lines+markers',
        name='Pasajeros',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=8, color='#00d4ff')
    ))
    
    fig.add_trace(go.Scatter(
        x=data['months'],
        y=data['operations'],
        mode='lines+markers',
        name='Operaciones',
        line=dict(color='#f59e0b', width=3),
        marker=dict(size=8, color='#f59e0b')
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Mes'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Participación (%)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

@callback(Output('progress-gauge', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_progress_gauge(n):
    current = 12.8
    target = 15.0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Meta 15%", 'font': {'color': 'white'}},
        delta={'reference': target},
        gauge={
            'axis': {'range': [None, 20]},
            'bar': {'color': "#00d4ff"},
            'steps': [
                {'range': [0, 10], 'color': "rgba(255,71,87,0.3)"},
                {'range': [10, 15], 'color': "rgba(245,158,11,0.3)"},
                {'range': [15, 20], 'color': "rgba(0,255,136,0.3)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target
            }
        }
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

@callback(Output('airport-comparison-chart', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_airport_comparison(n):
    data = get_airport_comparison()
    
    fig = go.Figure()
    
    colors = ['#ff4757' if x['change'] < 0 else '#00ff88' for x in data]
    
    fig.add_trace(go.Bar(
        x=[x['name'] for x in data],
        y=[x['passengers'] for x in data],
        marker_color='#00d4ff',
        text=[f"{x['passengers']}%" for x in data],
        textposition='auto',
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Aeropuerto'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Participación (%)'),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

# Callback for live time update
@callback(Output('live-update-time', 'children'),
          Input('interval-component', 'n_intervals'))
def update_time(n):
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

if __name__ == '__main__':
    print("🚀 Iniciando AIFA Dashboard...")
    print("📊 Dashboard ejecutivo cargando...")
    print("🌐 Acceso: http://localhost:8050")
    print("✅ Presiona Ctrl+C para detener")
    
    app.run_server(debug=True, host='0.0.0.0', port=8050)