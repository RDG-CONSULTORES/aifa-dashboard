#!/usr/bin/env python3
"""
AIFA Dashboard - Production Ready Version
Executive Dashboard for Felipe Ángeles International Airport
"""

import dash
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Initialize Dash app
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

# Simulated data functions
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
    cargo = [5.1, 5.4, 5.8, 6.2, 6.7, 7.1, 7.5, 7.8, 8.0, 8.1, 8.2, 8.4]
    return {'months': months, 'passengers': passengers, 'operations': operations, 'cargo': cargo}

def get_route_data():
    return [
        {'city': 'Los Angeles, USA', 'passengers': 87000, 'load_factor': 85.7, 'frequency': 21},
        {'city': 'Houston, USA', 'passengers': 76000, 'load_factor': 81.3, 'frequency': 19},
        {'city': 'Miami, USA', 'passengers': 92000, 'load_factor': 87.4, 'frequency': 17},
        {'city': 'Guadalajara, México', 'passengers': 125000, 'load_factor': 82.3, 'frequency': 42},
        {'city': 'Monterrey, México', 'passengers': 98000, 'load_factor': 78.5, 'frequency': 35},
        {'city': 'Cancún, México', 'passengers': 156000, 'load_factor': 89.2, 'frequency': 28},
        {'city': 'Bogotá, Colombia', 'passengers': 45000, 'load_factor': 79.8, 'frequency': 14},
        {'city': 'Lima, Perú', 'passengers': 38000, 'load_factor': 82.1, 'frequency': 10}
    ]

def get_airport_comparison():
    return [
        {'name': 'AICM', 'passengers': 48.2, 'change': -2.1},
        {'name': 'AIFA', 'passengers': 12.8, 'change': 2.3},
        {'name': 'Guadalajara', 'passengers': 8.9, 'change': 0.8},
        {'name': 'Cancún', 'passengers': 15.4, 'change': 1.2},
        {'name': 'Monterrey', 'passengers': 7.2, 'change': -0.3},
        {'name': 'Tijuana', 'passengers': 4.9, 'change': 0.5},
        {'name': 'Otros', 'passengers': 2.6, 'change': -0.4}
    ]

def get_financial_data():
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    revenue = [150, 162, 175, 188, 195, 210, 225, 238, 245, 260, 275, 290]
    costs = [112, 118, 125, 135, 140, 150, 160, 170, 175, 185, 195, 205]
    return {'months': months, 'revenue': revenue, 'costs': costs}

def get_capacity_data():
    return {
        'checkin_area': {'current': 245, 'utilization': 98, 'standard': 250, 'unit': 'm²/millón pax'},
        'waiting_area': {'current': 890, 'utilization': 82, 'standard': 900, 'unit': 'm²/millón pax'},
        'security_area': {'current': 120, 'utilization': 76, 'standard': 140, 'unit': 'm²/millón pax'},
        'sterile_area': {'current': 450, 'utilization': 85, 'standard': 500, 'unit': 'm²/millón pax'},
        'baggage_system': {'current': 2400, 'utilization': 80, 'max_capacity': 3000, 'unit': 'bags/hr'}
    }

def get_capacity_zones():
    return [
        {'zone': 'Terminal A - Check-in', 'utilization': 85, 'capacity': 12000, 'current': 10200},
        {'zone': 'Terminal A - Seguridad', 'utilization': 76, 'capacity': 8000, 'current': 6080},
        {'zone': 'Terminal B - Check-in', 'utilization': 92, 'capacity': 10000, 'current': 9200},
        {'zone': 'Terminal B - Seguridad', 'utilization': 68, 'capacity': 6000, 'current': 4080},
        {'zone': 'Sala de Espera Dom.', 'utilization': 82, 'capacity': 15000, 'current': 12300},
        {'zone': 'Sala de Espera Int.', 'utilization': 74, 'capacity': 8000, 'current': 5920},
        {'zone': 'Puertas de Embarque', 'utilization': 78, 'capacity': 25000, 'current': 19500},
        {'zone': 'Recogida Equipajes', 'utilization': 83, 'capacity': 12000, 'current': 9960}
    ]

def get_security_data():
    return {
        'runway_incidents': {'rate': 0.12, 'target': 0.15, 'unit': '/1000 ops', 'trend': -0.02},
        'fatal_accidents': {'rate': 0.00, 'target': 0.00, 'unit': '/1000 ops', 'trend': 0.00},
        'work_accidents': {'rate': 0.03, 'target': 0.05, 'unit': '/1000 hrs', 'trend': -0.01},
        'runway_incursions': {'rate': 0.05, 'target': 0.10, 'unit': '/1000 ops', 'trend': 0.01},
        'bird_strikes': {'rate': 0.85, 'target': 1.00, 'unit': '/1000 ops', 'trend': -0.15},
        'security_staff': {'ratio': 45, 'standard': 40, 'unit': '/millón pax', 'trend': 2},
        'fod_reports': {'rate': 1.2, 'target': 1.0, 'unit': '/1000 ops', 'trend': 0.2},
        'safety_score': {'score': 94.5, 'target': 95.0, 'unit': '/100', 'trend': 1.2}
    }

def get_quality_data():
    return {
        'security_time': {'avg': 6.4, 'target': 8.0, 'unit': 'min', 'trend': -0.3},
        'checkin_time': {'avg': 3.2, 'target': 5.0, 'unit': 'min', 'trend': -0.1},
        'baggage_time': {'avg': 8.1, 'target': 12.0, 'unit': 'min', 'trend': 0.4},
        'nps_score': {'score': 67, 'target': 50, 'unit': '/100', 'trend': 3},
        'satisfaction': {'score': 4.6, 'target': 4.0, 'unit': '/5', 'trend': 0.1},
        'cleanliness': {'score': 4.5, 'target': 4.0, 'unit': '/5', 'trend': 0.2}
    }

def get_productivity_data():
    return {
        'pax_per_employee': {'value': 1240, 'benchmark': 1100, 'unit': '/año', 'trend': 45},
        'ops_per_employee': {'value': 285, 'benchmark': 250, 'unit': '/año', 'trend': 12},
        'cargo_per_employee': {'value': 45, 'benchmark': 40, 'unit': 'tons/año', 'trend': 2},
        'gate_utilization': {'value': 78, 'target': 75, 'unit': '%', 'trend': 3},
        'aircraft_rotation': {'value': 11.2, 'benchmark': 10.0, 'unit': '/día', 'trend': 0.4}
    }

def get_route_network_data():
    """Datos de la red de rutas AIFA con coordenadas geográficas"""
    aifa_lat, aifa_lon = 19.7373, -99.0068
    
    return {
        'hub': {'name': 'AIFA', 'lat': aifa_lat, 'lon': aifa_lon},
        'routes': [
            {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "pax": 87000, "type": "international", "flights": 21},
            {"name": "Houston", "lat": 29.7604, "lon": -95.3698, "pax": 76000, "type": "international", "flights": 19},
            {"name": "Miami", "lat": 25.7617, "lon": -80.1918, "pax": 92000, "type": "international", "flights": 17},
            {"name": "Guadalajara", "lat": 20.6597, "lon": -103.3496, "pax": 125000, "type": "domestic", "flights": 42},
            {"name": "Monterrey", "lat": 25.6866, "lon": -100.3161, "pax": 98000, "type": "domestic", "flights": 35},
            {"name": "Cancún", "lat": 21.1619, "lon": -86.8515, "pax": 156000, "type": "domestic", "flights": 28},
            {"name": "Madrid", "lat": 40.4168, "lon": -3.7038, "pax": 67000, "type": "international", "flights": 14},
            {"name": "Bogotá", "lat": 4.7110, "lon": -74.0721, "pax": 45000, "type": "international", "flights": 12}
        ]
    }

# KPI Card component
def create_kpi_card(title, value, change, icon, target=None, unit="", format_type="percent"):
    trend_color = '#00ff88' if change > 0 else '#ff4757'
    trend_arrow = '↗' if change > 0 else '↘'
    
    if format_type == "percent":
        value_display = f"{value}%"
        change_display = f"{change:+.1f}%"
    elif format_type == "decimal":
        value_display = f"{value:.2f}{unit}"
        change_display = f"{change:+.2f}"
    elif format_type == "integer":
        value_display = f"{value:,}{unit}"
        change_display = f"{change:+.0f}"
    else:
        value_display = f"{value}{unit}"
        change_display = f"{change:+.1f}"
    
    progress = (value / target * 100) if target else None
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Div([
                    DashIconify(icon=icon, width=30, height=30, style={'color': '#00d4ff'})
                ], className="kpi-icon"),
                html.Div([
                    html.H6(title, className="kpi-title"),
                    html.H3(value_display, className="kpi-value"),
                    html.Div([
                        html.Span(trend_arrow, style={'color': trend_color, 'fontSize': '16px'}),
                        html.Span(change_display, style={'color': trend_color, 'marginLeft': '5px'})
                    ], className="kpi-change"),
                    html.Small("vs mes anterior", className="kpi-period")
                ], className="kpi-content")
            ], className="kpi-header"),
            
            # Progress bar if target exists
            html.Div([
                dbc.Progress(
                    value=progress if progress else 0,
                    color="info" if progress and progress >= 90 else "warning" if progress and progress >= 70 else "danger",
                    style={'height': '4px', 'background': 'rgba(255,255,255,0.1)'}
                ) if target else None,
                html.Small(f"Meta: {target}{unit if format_type != 'percent' else '%'}" if target else "", className="kpi-target")
            ], className="kpi-progress") if target else None
        ])
    ], className="kpi-card")

# Enhanced destination card for geographic tab
def create_enhanced_destination_card(route):
    """Crear tarjeta mejorada de destino con glassmorphism"""
    return html.Div([
        html.Div([
            html.Div([
                html.H6(route['city'], style={
                    'color': '#ffffff', 
                    'margin': '0 0 0.5rem 0', 
                    'fontWeight': '600',
                    'fontSize': '0.95rem'
                }),
                html.Div([
                    html.Span(f"{route['passengers']:,}", style={
                        'color': '#00d4ff', 
                        'fontWeight': '700',
                        'fontSize': '1.1rem'
                    }),
                    html.Span(" pax/año", style={
                        'color': '#8b92a9', 
                        'fontSize': '0.8rem',
                        'marginLeft': '4px'
                    })
                ], style={'marginBottom': '0.25rem'}),
            ], className="destination-info"),
            html.Div([
                html.Div(f"{route['load_factor']}%", style={
                    'color': '#f59e0b',
                    'fontWeight': '600',
                    'fontSize': '0.9rem'
                }),
                html.Div("Load Factor", style={
                    'color': '#8b92a9',
                    'fontSize': '0.7rem'
                })
            ], className="destination-metric")
        ], className="destination-row"),
        
        html.Div([
            html.Span("📅", style={'marginRight': '6px', 'fontSize': '0.8rem'}),
            html.Span(f"{route['frequency']} vuelos/mes", style={
                'color': '#8b92a9',
                'fontSize': '0.75rem'
            }),
            html.Span(" | ", style={
                'color': '#8b92a9',
                'margin': '0 6px'
            }),
            html.Span("✈️", style={'marginRight': '4px', 'fontSize': '0.8rem'}),
            html.Span(f"{route['frequency']//4} vuelos/sem", style={
                'color': '#8b92a9',
                'fontSize': '0.75rem'
            })
        ], className="destination-details")
    ], className="enhanced-destination-card")

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.Div([
                html.Img(
                    src="/assets/aifa-logo.jpg",
                    height="50px",
                    style={
                        'marginRight': '15px',
                        'backgroundColor': 'transparent',
                        'isolation': 'isolate'
                    },
                    className="header-logo"
                ),
                html.Div([
                    html.H1("Centro de Operaciones AIFA", className="header-title"),
                    html.P("Aeropuerto Internacional Felipe Ángeles", className="header-subtitle")
                ], className="header-text")
            ], className="header-content"),
            html.Div([
                html.Div([
                    html.Span("Última actualización: ", className="update-label"),
                    html.Span(id="live-update-time", className="update-time")
                ], className="update-info"),
                dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0)
            ], className="header-right")
        ], className="header-container")
    ], className="header"),
    
    # Navigation tabs
    dbc.Tabs([
        dbc.Tab(label="KPIs Estratégicos", tab_id="strategic", 
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Análisis Geográfico", tab_id="geographic",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Análisis Financiero", tab_id="financial",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Capacidad Operativa", tab_id="capacity",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Seguridad", tab_id="security",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Calidad de Servicio", tab_id="quality",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Productividad", tab_id="productivity",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'})
    ], id="tabs", active_tab="strategic", className="nav-tabs"),
    
    # Tab content
    html.Div(id="tab-content", className="content-area")
])

# Tab content callback
@callback(Output("tab-content", "children"),
          Input("tabs", "active_tab"))
def render_tab_content(active_tab):
    if active_tab == "strategic":
        return render_strategic_tab()
    elif active_tab == "geographic":
        return render_geographic_tab()
    elif active_tab == "financial":
        return render_financial_tab()
    elif active_tab == "capacity":
        return render_capacity_tab()
    elif active_tab == "security":
        return render_security_tab()
    elif active_tab == "quality":
        return render_quality_tab()
    elif active_tab == "productivity":
        return render_productivity_tab()
    else:
        return html.Div([
            html.H4(f"Módulo: {active_tab.replace('_', ' ').title()}", 
                   style={'color': '#8b92a9', 'textAlign': 'center', 'marginTop': '50px'}),
            html.P("En desarrollo - Framework implementado", 
                  style={'color': '#8b92a9', 'textAlign': 'center'})
        ])

def render_strategic_tab():
    kpi_data = get_kpi_data()
    
    return html.Div([
        # KPI Cards Row 1
        dbc.Row([
            dbc.Col([
                create_kpi_card(
                    "Participación Nacional Pasajeros",
                    kpi_data['participation_passengers']['current'],
                    kpi_data['participation_passengers']['change'],
                    "mdi:account-group",
                    kpi_data['participation_passengers']['target']
                )
            ], width=4),
            dbc.Col([
                create_kpi_card(
                    "Participación Nacional Operaciones",
                    kpi_data['participation_operations']['current'],
                    kpi_data['participation_operations']['change'],
                    "mdi:airplane-takeoff",
                    kpi_data['participation_operations']['target']
                )
            ], width=4),
            dbc.Col([
                create_kpi_card(
                    "Participación Nacional Carga",
                    kpi_data['participation_cargo']['current'],
                    kpi_data['participation_cargo']['change'],
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
                    "mdi:trending-up"
                )
            ], width=4),
            dbc.Col([
                create_kpi_card(
                    "Puntualidad de Vuelos",
                    kpi_data['punctuality']['current'],
                    kpi_data['punctuality']['change'],
                    "mdi:clock-check-outline",
                    kpi_data['punctuality']['target']
                )
            ], width=4),
            dbc.Col([
                create_kpi_card(
                    "Utilización de Rutas",
                    kpi_data['route_utilization']['current'],
                    kpi_data['route_utilization']['change'],
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

def render_geographic_tab():
    route_data = get_route_data()
    
    return html.Div([
        html.H4("Análisis Geográfico", className="page-title"),
        html.P("Red de destinos, rutas estratégicas y análisis de mercado", className="page-subtitle"),
        
        # KPIs Geográficos Row 1
        dbc.Row([
            dbc.Col([
                create_kpi_card("Destinos Activos", 28, 3, "material-symbols:flight", None, "", "integer")
            ], width=2),
            dbc.Col([
                create_kpi_card("Países", 8, 2, "material-symbols:public", None, "", "integer")
            ], width=2),
            dbc.Col([
                create_kpi_card("Rutas Internacionales", 12, 4, "material-symbols:connecting-airports", None, "", "integer")
            ], width=2),
            dbc.Col([
                create_kpi_card("Rutas Domésticas", 16, 1, "material-symbols:home", None, "", "integer")
            ], width=2),
            dbc.Col([
                create_kpi_card("Nuevas Rutas 2024", 7, 7, "material-symbols:new-releases", None, "", "integer")
            ], width=2),
            dbc.Col([
                create_kpi_card("Factor Carga Prom.", 84.2, 2.1, "material-symbols:analytics", None, "%", "decimal")
            ], width=2)
        ], className="mb-4"),
        
        # Red Global de Rutas
        dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.H5("Red Global de Rutas AIFA", className="chart-title"),
                    html.Div([
                        dbc.ButtonGroup([
                            dbc.Button("Todas", id="route-filter-all", size="sm", 
                                      className="filter-btn active", color="info", outline=True),
                            dbc.Button("Internacionales", id="route-filter-intl", size="sm", 
                                      className="filter-btn", color="info", outline=True),
                            dbc.Button("Domésticas", id="route-filter-dom", size="sm", 
                                      className="filter-btn", color="info", outline=True),
                        ])
                    ])
                ], className="d-flex justify-content-between align-items-center")
            ]),
            dbc.CardBody([
                dcc.Graph(id="route-network-map", style={"height": "500px"})
            ])
        ], className="chart-card mb-4"),
        
        # Panel de Destinos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Principales Destinos", className="chart-title"),
                        html.Small("Red de rutas y conexiones AIFA", className="chart-subtitle")
                    ]),
                    dbc.CardBody([
                        html.Div([
                            create_enhanced_destination_card(route) for route in route_data
                        ])
                    ])
                ], className="chart-card")
            ], width=12)
        ], className="mb-4"),
        
        # Gráficas Simplificadas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Distribución por Región", className="chart-title"),
                        html.Small("Tráfico de pasajeros por zona geográfica", className="chart-subtitle")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="geographic-distribution-chart")
                    ])
                ], className="chart-card")
            ], width=12)
        ])
    ])

def render_financial_tab():
    financial_data = get_financial_data()
    
    return html.Div([
        html.H4("Análisis Financiero", className="page-title"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Ingresos Mensuales", style={'color': 'white'}),
                        html.H2("$290M MXN", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.Div([
                            html.Span("↗", style={'color': '#00ff88', 'fontSize': '1.2rem'}),
                            html.Span(" +5.4% vs mes anterior", style={'color': '#00ff88', 'marginLeft': '0.5rem'})
                        ])
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Margen EBITDA", style={'color': 'white'}),
                        html.H2("29.3%", style={'color': '#f59e0b', 'margin': '1rem 0'}),
                        html.Div([
                            html.Span("↗", style={'color': '#00ff88', 'fontSize': '1.2rem'}),
                            html.Span(" +1.8% vs mes anterior", style={'color': '#00ff88', 'marginLeft': '0.5rem'})
                        ])
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("ROI Anual", style={'color': 'white'}),
                        html.H2("22.1%", style={'color': '#00ff88', 'margin': '1rem 0'}),
                        html.Div([
                            html.Span("↗", style={'color': '#00ff88', 'fontSize': '1.2rem'}),
                            html.Span(" +3.2% vs año anterior", style={'color': '#00ff88', 'marginLeft': '0.5rem'})
                        ])
                    ])
                ], className="chart-card")
            ], width=4)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Evolución Financiera", className="chart-title"),
                        html.Small("Ingresos vs Costos (Millones MXN)", className="chart-subtitle")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="financial-trend-chart")
                    ])
                ], className="chart-card")
            ], width=12)
        ])
    ])

def render_capacity_tab():
    return html.Div([
        html.H4("🚀 Capacidad Operativa (FORCE DEPLOY v2.2)", className="page-title", style={'color': 'white'}),
        html.P("Version: 2.2 - FORCE REDEPLOY - Si ves esto, el deploy funcionó", style={'color': '#f59e0b', 'fontSize': '0.9rem', 'marginBottom': '1rem'}),
        
        # Simple KPI Cards Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Área Check-in", style={'color': 'white'}),
                        html.H2("245 m²", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("98% utilización", style={'color': '#8b92a9'})
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Salas de Espera", style={'color': 'white'}),
                        html.H2("890 m²", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("82% utilización", style={'color': '#8b92a9'})
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Controles Seguridad", style={'color': 'white'}),
                        html.H2("120 m²", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("76% utilización", style={'color': '#8b92a9'})
                    ])
                ], className="chart-card")
            ], width=4)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Sistema de Equipajes", style={'color': 'white'}),
                        html.H2("2,400 bags/hr", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Capacidad máxima: 3,000 bags/hr", style={'color': '#8b92a9'})
                    ])
                ], className="chart-card")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Área Estéril", style={'color': 'white'}),
                        html.H2("450 m²", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("85% utilización", style={'color': '#8b92a9'})
                    ])
                ], className="chart-card")
            ], width=6)
        ])
    ])

def render_security_tab():
    return html.Div([
        html.H4("Seguridad Operacional", className="page-title", style={'color': 'white'}),
        
        # Simple KPI Cards Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Incidentes Pista", style={'color': 'white'}),
                        html.H2("0.12/1000 ops", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Meta: <0.15/1000 ops", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Accidentes Mortales", style={'color': 'white'}),
                        html.H2("0.00/1000 ops", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Excelente", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Choques Aves", style={'color': 'white'}),
                        html.H2("0.85/1000 ops", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Dentro del estándar", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Score General", style={'color': 'white'}),
                        html.H2("94.5/100", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Excelente", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=3)
        ], className="mb-4"),
        
        # Additional KPIs
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Personal Seguridad", style={'color': 'white'}),
                        html.H2("45/millón pax", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Sobre estándar (40)", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Incursiones Pista", style={'color': 'white'}),
                        html.H2("0.05/1000 ops", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Bajo el límite", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=6)
        ])
    ])

def render_quality_tab():
    return html.Div([
        html.H4("Calidad de Servicio", className="page-title", style={'color': 'white'}),
        
        # KPI Cards Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Tiempo Control Seguridad", style={'color': 'white'}),
                        html.H2("6.4 min", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Meta: <8 min", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Tiempo Check-in", style={'color': 'white'}),
                        html.H2("3.2 min", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Meta: <5 min", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Tiempo Espera Equipaje", style={'color': 'white'}),
                        html.H2("8.1 min", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Meta: <12 min", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=4)
        ], className="mb-4"),
        
        # KPI Cards Row 2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("NPS Score", style={'color': 'white'}),
                        html.H2("67/100", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Excelente (>50)", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Satisfacción General", style={'color': 'white'}),
                        html.H2("4.6/5", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("92% satisfacción", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Limpieza Baños", style={'color': 'white'}),
                        html.H2("4.5/5", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("90% satisfacción", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=4)
        ])
    ])

def render_productivity_tab():
    return html.Div([
        html.H4("Productividad Operacional", className="page-title", style={'color': 'white'}),
        
        # KPI Cards Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Pasajeros por Empleado", style={'color': 'white'}),
                        html.H2("1,240/año", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Benchmark: 1,100/año", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Operaciones por Empleado", style={'color': 'white'}),
                        html.H2("285/año", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Benchmark: 250/año", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Carga por Empleado", style={'color': 'white'}),
                        html.H2("45 tons/año", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Benchmark: 40 tons/año", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=4)
        ], className="mb-4"),
        
        # KPI Cards Row 2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Utilización Puertas", style={'color': 'white'}),
                        html.H2("78%", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Meta: 75%", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Rotación Aeronaves", style={'color': 'white'}),
                        html.H2("11.2/día", style={'color': '#00d4ff', 'margin': '1rem 0'}),
                        html.P("Benchmark: 10.0/día", style={'color': '#00ff88'})
                    ])
                ], className="chart-card")
            ], width=6)
        ])
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
    
    fig.add_trace(go.Scatter(
        x=data['months'],
        y=data['cargo'],
        mode='lines+markers',
        name='Carga',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=8, color='#00ff88')
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

@callback(Output('financial-trend-chart', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_financial_trend(n):
    data = get_financial_data()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data['months'],
        y=data['revenue'],
        name='Ingresos',
        marker_color='#00d4ff'
    ))
    
    fig.add_trace(go.Bar(
        x=data['months'],
        y=data['costs'],
        name='Costos',
        marker_color='#ff4757'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Mes'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Millones MXN'),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

# Removed unused callbacks for non-existent chart IDs

# Geographic Tab Callback - Simplified
@callback(Output('geographic-distribution-chart', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_geographic_distribution(n):
    route_data = get_route_data()
    
    # Agrupar por región
    regions = {'USA': 0, 'México': 0, 'LATAM': 0}
    for route in route_data:
        if 'USA' in route['city']:
            regions['USA'] += route['passengers']
        elif 'México' in route['city']:
            regions['México'] += route['passengers']
        else:
            regions['LATAM'] += route['passengers']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(regions.keys()),
        y=list(regions.values()),
        marker=dict(
            color=['#00d4ff', '#f59e0b', '#00ff88'],
        ),
        text=[f'{v:,}' for v in regions.values()],
        textposition='auto'
    ))
    
    fig.update_layout(
        xaxis=dict(title='Región', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Pasajeros Anuales', gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig

# Route Network Map Callbacks - Simplified version
@callback(
    Output('route-network-map', 'figure'),
    [Input('route-filter-all', 'n_clicks'),
     Input('route-filter-intl', 'n_clicks'),
     Input('route-filter-dom', 'n_clicks')]
)
def update_route_network(all_clicks, intl_clicks, dom_clicks):
    """Actualiza el mapa de rutas según el filtro seleccionado"""
    try:
        # Determinar filtro activo de manera simple
        ctx = dash.callback_context
        filter_type = 'all'  # Por defecto mostrar todas
        
        # Si hay context y fue triggereado, determinar qué botón
        if ctx.triggered and ctx.triggered[0]['prop_id'] != '.':
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'route-filter-intl':
                filter_type = 'international'
            elif button_id == 'route-filter-dom':
                filter_type = 'domestic'
        
        # Obtener datos
        data = get_route_network_data()
        hub = data['hub']
        routes = data['routes']
        
        # Aplicar filtro
        if filter_type == 'international':
            routes = [r for r in routes if r['type'] == 'international']
        elif filter_type == 'domestic':
            routes = [r for r in routes if r['type'] == 'domestic']
        
        # Crear figura
        fig = go.Figure()
        
        # 1. Hub AIFA - Marker central premium
        fig.add_trace(go.Scattergeo(
            lat=[hub['lat']],
            lon=[hub['lon']],
            text=['✈️ AIFA HUB'],
            mode='markers+text',
            marker=dict(
                size=45,
                color='#f59e0b',  # Color dorado para destacar
                line=dict(width=6, color='white'),
                symbol='star',
                opacity=1.0
            ),
            textposition='bottom center',
            textfont=dict(size=16, color='white', family='Inter'),
            name='AIFA Hub',
            hovertemplate='<b>🛬 AIFA - Hub Principal</b><br>📍 Felipe Ángeles International<br>🌐 Rutas Activas: ' + str(len(routes)) + '<br>📊 Estado: Operacional<extra></extra>'
        ))
        
        # 2. Líneas de rutas - Mejoradas para mayor visibilidad
        for route in routes:
            # Colores más contrastantes y visibles
            if route['type'] == 'international':
                line_color = '#00d4ff'  # Azul brillante para internacionales
                line_dash = 'solid'
            else:
                line_color = '#00ff88'  # Verde brillante para domésticas  
                line_dash = 'solid'
            
            # Grosor basado en volumen pero más grueso
            line_width = max(4, min(route['pax']/20000, 12))  # Entre 4 y 12px
            
            fig.add_trace(go.Scattergeo(
                lat=[hub['lat'], route['lat']],
                lon=[hub['lon'], route['lon']],
                mode='lines',
                line=dict(
                    width=line_width,
                    color=line_color,
                    opacity=1.0,  # Opacity completa para máxima visibilidad
                    dash=line_dash
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # 3. Markers de destinos - Rediseñados para mayor visibilidad
        for route in routes:
            # Tamaños más grandes y distintivos
            marker_size = max(18, min(route['pax']/8000, 35))  # Entre 18 y 35px
            
            # Colores más vibrantes y diferenciados
            if route['type'] == 'international':
                marker_color = '#ff6b35'  # Naranja vibrante para internacionales
                marker_symbol = 'square'
            else:
                marker_color = '#00ff88'  # Verde brillante para domésticas
                marker_symbol = 'circle'
            
            fig.add_trace(go.Scattergeo(
                lat=[route['lat']],
                lon=[route['lon']],
                text=[route['name']],
                mode='markers+text',
                marker=dict(
                    size=marker_size,
                    color=marker_color,
                    line=dict(width=4, color='white'),  # Border más grueso
                    symbol=marker_symbol,
                    opacity=1.0
                ),
                textposition='top center',
                textfont=dict(size=11, color='white', family='Inter'),
                showlegend=False,
                hovertemplate='<b>🎯 ' + route['name'] + '</b><br>' +
                             '👥 Pasajeros: ' + f"{route['pax']:,}" + '/año<br>' +
                             '✈️ Vuelos: ' + str(route['flights']) + '/mes<br>' +
                             '🌐 Tipo: ' + route['type'].title() + '<br>' +
                             '📈 Load Factor: Excelente<extra></extra>'
            ))
        
        # Layout del mapa - Optimizado para mejor contraste
        fig.update_layout(
            geo=dict(
                scope='world',
                projection_type='natural earth',
                showland=True,
                landcolor='rgba(15, 20, 35, 0.95)',  # Más oscuro para contraste
                showocean=True,
                oceancolor='rgba(5, 10, 25, 0.98)',  # Océano más profundo
                showcountries=True,
                countrycolor='rgba(0, 212, 255, 0.6)',  # Borders más visibles
                coastlinecolor='rgba(0, 212, 255, 0.7)',
                showlakes=False,  # Eliminar lagos para simplificar
                bgcolor='rgba(0,0,0,0)',
                showframe=False,
                center=dict(lat=25, lon=-95),
                projection_scale=1.1,  # Zoom ligeramente menor
                resolution=50  # Mejor resolución
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Inter'),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            height=500,
            title=dict(
                text="",
                x=0.5,
                font=dict(size=18, color='white')
            )
        )
        
        return fig
        
    except Exception as e:
        # En caso de error, devolver mapa básico
        print(f"Error en update_route_network: {str(e)}")
        
        # Mapa de respaldo básico
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lat=[19.7373],
            lon=[-99.0068],
            text=['AIFA'],
            mode='markers+text',
            marker=dict(size=30, color='#00d4ff'),
            textposition='bottom center'
        ))
        
        fig.update_layout(
            geo=dict(
                scope='world',
                projection_type='natural earth',
                showland=True,
                landcolor='rgba(26, 31, 58, 0.8)',
                showocean=True,
                oceancolor='rgba(10, 14, 39, 0.9)',
                center=dict(lat=25, lon=-95)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500
        )
        
        return fig

@callback(
    [Output('route-filter-all', 'className'),
     Output('route-filter-intl', 'className'),
     Output('route-filter-dom', 'className')],
    [Input('route-filter-all', 'n_clicks'),
     Input('route-filter-intl', 'n_clicks'),
     Input('route-filter-dom', 'n_clicks')]
)
def update_filter_buttons(all_clicks, intl_clicks, dom_clicks):
    """Actualiza el estado activo de los botones de filtro"""
    try:
        ctx = dash.callback_context
        base_class = "filter-btn"
        active_class = "filter-btn active"
        
        # Por defecto, "Todas" está activo
        if not ctx.triggered or ctx.triggered[0]['prop_id'] == '.':
            return [active_class, base_class, base_class]
        
        # Determinar qué botón fue presionado
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'route-filter-all':
            return [active_class, base_class, base_class]
        elif button_id == 'route-filter-intl':
            return [base_class, active_class, base_class]
        elif button_id == 'route-filter-dom':
            return [base_class, base_class, active_class]
        else:
            return [active_class, base_class, base_class]
            
    except Exception as e:
        print(f"Error en update_filter_buttons: {str(e)}")
        # En caso de error, devolver estado por defecto
        return ["filter-btn active", "filter-btn", "filter-btn"]

# Time update callback
@callback(Output('live-update-time', 'children'),
          Input('interval-component', 'n_intervals'))
def update_time(n):
    from datetime import datetime
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)