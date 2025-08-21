import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from ..data.simulated_data import generate_kpi_data, generate_historical_data, generate_airport_comparison

def create_kpi_card(title, value, change, trend, icon, target=None):
    """Create a KPI card component"""
    trend_color = '#00ff88' if trend == 'up' else '#ff4757'
    trend_icon = 'mdi:arrow-up' if trend == 'up' else 'mdi:arrow-down'
    
    progress = (value / target * 100) if target else None
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Div([
                    DashIconify(icon=icon, width=30, height=30, style={'color': '#00d4ff'})
                ], className="kpi-icon"),
                html.Div([
                    html.H6(title, className="kpi-title"),
                    html.H3(f"{value}%", className="kpi-value"),
                    html.Div([
                        DashIconify(icon=trend_icon, width=16, height=16, style={'color': trend_color}),
                        html.Span(f"{change:+.1f}%", style={'color': trend_color, 'marginLeft': '5px'})
                    ], className="kpi-change"),
                    html.Small(f"vs mes anterior", className="kpi-period")
                ], className="kpi-content")
            ], className="kpi-header"),
            
            # Progress bar if target exists
            html.Div([
                dbc.Progress(
                    value=progress if progress else 0,
                    color="info" if progress and progress >= 90 else "warning" if progress and progress >= 70 else "danger",
                    style={'height': '4px', 'background': 'rgba(255,255,255,0.1)'}
                ) if target else None,
                html.Small(f"Meta: {target}%" if target else "", className="kpi-target")
            ], className="kpi-progress") if target else None
        ])
    ], className="kpi-card")

# Generate data
kpi_data = generate_kpi_data()
historical_data = generate_historical_data()
comparison_data = generate_airport_comparison()

# Layout
layout = html.Div([
    # KPI Cards Row
    dbc.Row([
        dbc.Col([
            create_kpi_card(
                "Participación Nacional Pasajeros",
                kpi_data['participation_passengers']['current'],
                kpi_data['participation_passengers']['change'],
                kpi_data['participation_passengers']['trend'],
                "mdi:account-group",
                kpi_data['participation_passengers']['target']
            )
        ], width=4),
        dbc.Col([
            create_kpi_card(
                "Participación Nacional Operaciones",
                kpi_data['participation_operations']['current'],
                kpi_data['participation_operations']['change'],
                kpi_data['participation_operations']['trend'],
                "mdi:airplane-takeoff",
                kpi_data['participation_operations']['target']
            )
        ], width=4),
        dbc.Col([
            create_kpi_card(
                "Participación Nacional Carga",
                kpi_data['participation_cargo']['current'],
                kpi_data['participation_cargo']['change'],
                kpi_data['participation_cargo']['trend'],
                "mdi:package-variant",
                kpi_data['participation_cargo']['target']
            )
        ], width=4)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            create_kpi_card(
                "Crecimiento vs Mercado",
                kpi_data['growth_vs_market']['current'],
                kpi_data['growth_vs_market']['change'],
                kpi_data['growth_vs_market']['trend'],
                "mdi:trending-up"
            )
        ], width=4),
        dbc.Col([
            create_kpi_card(
                "Puntualidad de Vuelos",
                kpi_data['punctuality']['current'],
                kpi_data['punctuality']['change'],
                kpi_data['punctuality']['trend'],
                "mdi:clock-check-outline",
                kpi_data['punctuality']['target']
            )
        ], width=4),
        dbc.Col([
            create_kpi_card(
                "Utilización de Rutas",
                kpi_data['route_utilization']['current'],
                kpi_data['route_utilization']['change'],
                kpi_data['route_utilization']['trend'],
                "mdi:map-marker-path",
                kpi_data['route_utilization']['target']
            )
        ], width=4)
    ], className="mb-4"),
    
    # Charts Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Evolución Participación de Mercado", className="chart-title"),
                    html.Small("Últimos 12 meses", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    dcc.Graph(id="participation-trend-chart")
                ])
            ], className="chart-card")
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Progreso Meta Anual", className="chart-title"),
                    html.Small("Participación de pasajeros", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    dcc.Graph(id="progress-gauge")
                ])
            ], className="chart-card")
        ], width=4)
    ], className="mb-4"),
    
    # Comparison Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Comparativo Aeropuertos Mexicanos", className="chart-title"),
                    html.Small("Participación de mercado nacional", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    dcc.Graph(id="airport-comparison-chart")
                ])
            ], className="chart-card")
        ], width=12)
    ])
])

# Callbacks for charts
@callback(
    Output('participation-trend-chart', 'figure'),
    Input('participation-trend-chart', 'id')
)
def update_participation_trend(_):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=historical_data['date'],
        y=historical_data['passengers'],
        mode='lines+markers',
        name='Pasajeros',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=8, color='#00d4ff')
    ))
    
    fig.add_trace(go.Scatter(
        x=historical_data['date'],
        y=historical_data['operations'],
        mode='lines+markers',
        name='Operaciones',
        line=dict(color='#f59e0b', width=3),
        marker=dict(size=8, color='#f59e0b')
    ))
    
    fig.add_trace(go.Scatter(
        x=historical_data['date'],
        y=historical_data['cargo'],
        mode='lines+markers',
        name='Carga',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=8, color='#00ff88')
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.1)',
            title='Participación (%)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

@callback(
    Output('progress-gauge', 'figure'),
    Input('progress-gauge', 'id')
)
def update_progress_gauge(_):
    current = kpi_data['participation_passengers']['current']
    target = kpi_data['participation_passengers']['target']
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = current,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Meta 15%"},
        delta = {'reference': target},
        gauge = {
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

@callback(
    Output('airport-comparison-chart', 'figure'),
    Input('airport-comparison-chart', 'id')
)
def update_airport_comparison(_):
    fig = go.Figure()
    
    colors = ['#ff4757' if x < 0 else '#00ff88' for x in comparison_data['change']]
    
    fig.add_trace(go.Bar(
        x=comparison_data['name'],
        y=comparison_data['passengers'],
        name='Participación Pasajeros (%)',
        marker_color='#00d4ff',
        text=comparison_data['passengers'],
        textposition='auto',
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title='Aeropuerto'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title='Participación (%)'
        ),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig