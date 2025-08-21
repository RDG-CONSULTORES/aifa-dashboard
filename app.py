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
    """Datos completos de los 15 KPIs de seguridad operacional AIFA"""
    return {
        # KPIs principales (Top 5)
        'runway_incidents': {'rate': 0.12, 'target': '<0.15', 'unit': '/1000 ops', 'status': 'excellent', 'trend': -0.02},
        'fatal_accidents': {'rate': 0.00, 'target': '0.00', 'unit': '/1000 ops', 'status': 'excellent', 'trend': 0.00},
        'work_accidents': {'rate': 0.03, 'target': '<0.05', 'unit': '/1000 hrs', 'status': 'excellent', 'trend': -0.01},
        'runway_incursions': {'rate': 0.05, 'target': '<0.10', 'unit': '/1000 ops', 'status': 'excellent', 'trend': 0.01},
        'bird_strikes': {'rate': 0.85, 'target': '<1.20', 'unit': '/1000 ops', 'status': 'good', 'trend': 0.05},
        
        # Métricas operacionales (10 restantes)
        'security_staff': {'rate': 45, 'target': '>40', 'unit': '/millón pax', 'status': 'good', 'trend': 2.1},
        'incident_movements': {'rate': 0.08, 'target': '<0.12', 'unit': '/movimiento', 'status': 'excellent', 'trend': -0.02},
        'cameras_density': {'rate': 2.3, 'target': '>2.0', 'unit': '/hectárea', 'status': 'good', 'trend': 0.1},
        'wildlife_events': {'rate': 0.15, 'target': '<0.25', 'unit': '/operación', 'status': 'excellent', 'trend': -0.03},
        'lighting_functional': {'rate': 98.7, 'target': '>97.0', 'unit': '%', 'status': 'excellent', 'trend': 0.2},
        'lighting_incidents': {'rate': 0.02, 'target': '<0.05', 'unit': '/operación', 'status': 'excellent', 'trend': 0.01},
        'pothole_attended': {'rate': 95.2, 'target': '>90.0', 'unit': '%', 'status': 'excellent', 'trend': 1.8},
        'runway_maintenance': {'rate': 0.06, 'target': '<0.10', 'unit': '/operación', 'status': 'excellent', 'trend': -0.01},
        'fod_reports': {'rate': 0.08, 'target': '<0.15', 'unit': '/operación', 'status': 'excellent', 'trend': 0.02},
        'fod_damage': {'rate': 0.01, 'target': '<0.03', 'unit': '/operación', 'status': 'excellent', 'trend': 0.00}
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
            DashIconify(icon="mdi:calendar", width=16, height=16, style={'marginRight': '6px', 'color': '#8b92a9'}),
            html.Span(f"{route['frequency']} vuelos/mes", style={
                'color': '#8b92a9',
                'fontSize': '0.75rem'
            }),
            html.Span(" | ", style={
                'color': '#8b92a9',
                'margin': '0 6px'
            }),
            DashIconify(icon="mdi:airplane", width=16, height=16, style={'marginRight': '4px', 'color': '#8b92a9'}),
            html.Span(f"{route['frequency']//4} vuelos/sem", style={
                'color': '#8b92a9',
                'fontSize': '0.75rem'
            })
        ], className="destination-details")
    ], className="enhanced-destination-card")

# Operations Center Components
def create_capacity_gauge(title, percentage, value, benchmark, icon, status):
    """Crear gauge visual para capacidad operativa"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=40, height=40, className="capacity-gauge-icon"),
                html.Div([
                    html.H2(percentage, className="gauge-percentage"),
                    html.P(title, className="gauge-title"),
                    html.Small(value, className="gauge-value"),
                    html.Small(benchmark, className="gauge-benchmark")
                ])
            ], className="gauge-content"),
            
            # Progress ring visual
            html.Div([
                dbc.Progress(
                    value=int(percentage.replace('%', '')),
                    color=status,
                    className="capacity-progress-ring",
                    style={"height": "8px"}
                )
            ], className="mt-2")
        ])
    ], className="capacity-gauge-card")

def create_status_row(zone, capacity, utilization, throughput, wait_time, status):
    """Crear fila para la tabla de estado operativo"""
    utilization_value = int(utilization.replace('%', ''))
    status_colors = {"optimal": "success", "warning": "warning", "critical": "danger"}
    
    return html.Tr([
        html.Td(zone, className="zone-name"),
        html.Td(capacity),
        html.Td([
            dbc.Progress(
                value=utilization_value,
                color=status_colors[status],
                className="mb-1",
                style={"height": "8px"}
            ),
            html.Small(utilization)
        ]),
        html.Td(throughput),
        html.Td(wait_time),
        html.Td([
            dbc.Badge(status.upper(), color=status_colors[status])
        ])
    ])

# Security Operations Components
def create_security_kpi_card(title, value, unit, target, status, icon):
    """Crear KPI card para seguridad operacional"""
    status_colors = {
        "excellent": "#00ff88",
        "good": "#00d4ff", 
        "warning": "#f59e0b",
        "critical": "#ff4757"
    }
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=48, height=48, className="security-kpi-icon"),
                html.Div([
                    html.H3(f"{value}", className="security-kpi-value"),
                    html.P(unit, className="security-kpi-unit"),
                    html.H6(title, className="security-kpi-title"),
                    html.Small(f"Meta: {target}", className="security-target")
                ])
            ], className="security-kpi-content"),
            
            # Status indicator
            html.Div([
                dbc.Badge(status.upper(), color=status, className="security-status-badge")
            ], className="mt-2")
        ])
    ], className="security-kpi-card")

def create_security_gauge(title, percentage, critical_threshold, icon):
    """Crear gauge circular para métricas de seguridad"""
    # Asegurar que percentage sea entero
    percentage_val = int(float(percentage)) if isinstance(percentage, (str, float)) else percentage
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=36, height=36, className="security-gauge-icon"),
                html.H4(f"{percentage_val}%", className="security-gauge-percentage"),
                html.P(title, className="security-gauge-title"),
                html.Small(f"Crítico: >{critical_threshold}%", className="security-gauge-threshold")
            ], className="text-center"),
            
            # Circular progress
            dbc.Progress(
                value=percentage_val,
                color="success" if percentage_val < critical_threshold else "warning" if percentage_val < 90 else "danger",
                className="security-circular-progress",
                style={"height": "8px"}
            )
        ])
    ], className="security-gauge-card")

def create_airport_map_svg():
    """Crear mapa SVG del aeropuerto AIFA con zonas de seguridad"""
    return html.Div([
        html.Div([
            # Representación visual del aeropuerto con CSS
            html.Div([
                html.Div("Terminal AIFA", className="airport-terminal"),
                html.Div("Pista 12L/30R", className="airport-runway runway-1"),
                html.Div("Pista 12R/30L", className="airport-runway runway-2"),
                html.Div("Torre Control", className="control-tower"),
                
                # Zonas de seguridad
                html.Div(className="security-zone zone-1"),
                html.Div(className="security-zone zone-2"),
                html.Div(className="security-zone zone-3"),
                html.Div(className="security-zone zone-4"),
                
                # Cámaras de seguridad
                html.Div(className="security-camera cam-1"),
                html.Div(className="security-camera cam-2"),
                html.Div(className="security-camera cam-3"),
                html.Div(className="security-camera cam-4"),
            ], className="airport-layout")
        ], className="airport-visual-container")
    ], className="map-container")

def get_security_chart_layout():
    """Layout estándar para gráficos de seguridad"""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(10, 14, 39, 0.95)',
        'font': {'color': 'white', 'family': 'Inter', 'size': 12},
        'margin': {'l': 80, 'r': 40, 't': 40, 'b': 80},
        'xaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.15)', 'showgrid': True},
        'yaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.15)', 'showgrid': True},
        'legend': {'font': {'color': 'white'}, 'bgcolor': 'rgba(26, 31, 58, 0.9)'},
        'hovermode': 'x unified'
    }

# Bloomberg Terminal Components
def create_trading_card(label, value, change, trend):
    """Crear trading card estilo Bloomberg"""
    return dbc.Card([
        dbc.CardBody([
            html.P(label, className="trading-label"),
            html.H2(value, className="trading-value"),
            html.Div([
                DashIconify(
                    icon="mdi:trending-up" if trend == "positive" else "mdi:trending-down", 
                    width=20, height=20, 
                    className="me-2"
                ),
                change
            ], className=f"trading-change {trend}")
        ])
    ], className="trading-card")

def create_financial_kpi(title, value, change, icon):
    """Crear KPI financiero con icono"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=32, height=32, className="financial-icon"),
                html.Div([
                    html.H4(value, className="financial-kpi-value"),
                    html.P(title, className="financial-kpi-title"),
                    html.Small(change, className="financial-kpi-change")
                ])
            ], className="d-flex align-items-center")
        ])
    ], className="financial-kpi-card")

def create_financial_row(metric, current, target, variance, trend, industry, performance):
    """Crear fila para la matriz de rendimiento financiero"""
    trend_icon = "mdi:trending-up" if trend == "up" else "mdi:trending-down" if trend == "down" else "mdi:trending-neutral"
    trend_color = "text-success" if trend == "up" else "text-danger" if trend == "down" else "text-warning"
    
    return html.Tr([
        html.Td(metric, className="metric-name"),
        html.Td(current),
        html.Td(target),
        html.Td(variance, className="text-success" if "+" in variance else "text-danger"),
        html.Td([DashIconify(icon=trend_icon, width=16, height=16, className=trend_color)]),
        html.Td(industry),
        html.Td([
            dbc.Badge(
                "Excelente" if performance == "excellent" else "Bueno" if performance == "good" else "Advertencia",
                color="success" if performance == "excellent" else "info" if performance == "good" else "warning"
            )
        ])
    ])

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
        dbc.Tab(label="Control 360°", tab_id="control-360",
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
    elif active_tab == "control-360":
        return render_control_360_tab()
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
        
        # KPIs Geográficos - Grid 2x3 Balanceado y Responsive
        dbc.Row([
            dbc.Col([
                create_kpi_card("Destinos Activos", 28, 3, "mdi:map-marker-multiple", None, "", "integer")
            ], lg=4, md=6, sm=12),
            dbc.Col([
                create_kpi_card("Países Conectados", 8, 2, "mdi:earth", None, "", "integer")
            ], lg=4, md=6, sm=12),
            dbc.Col([
                create_kpi_card("Rutas Internacionales", 12, 4, "mdi:airplane", None, "", "integer")
            ], lg=4, md=6, sm=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                create_kpi_card("Rutas Domésticas", 16, 1, "mdi:home-map-marker", None, "", "integer")
            ], lg=4, md=6, sm=12),
            dbc.Col([
                create_kpi_card("Nuevas Rutas 2024", 7, 7, "mdi:plus-circle", None, "", "integer")
            ], lg=4, md=6, sm=12),
            dbc.Col([
                create_kpi_card("Factor Carga Promedio", 84.2, 2.1, "mdi:gauge", None, "%", "decimal")
            ], lg=4, md=6, sm=12)
        ], className="mb-4"),
        
        
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

def render_control_360_tab():
    """Renderiza el tab del Control 360° con la demo 3D interactiva"""
    return html.Div([
        html.H4("Control 360° - Red Global de Rutas AIFA", className="page-title"),
        html.P("Sistema de Navegación Ejecutiva | Tecnología Aeroportuaria Premium", 
               className="page-subtitle"),
        
        # Container principal para la demo 3D
        html.Div([
            # Iframe que carga la demo 3D routes
            html.Iframe(
                src="/assets/demo_3d_routes.html",
                className="control-360-iframe"
            )
        ], className="control-360-container")
    ])

def render_financial_tab():
    """Renderiza el tab financiero con estilo Bloomberg Terminal profesional"""
    return html.Div([
        # Bloomberg Terminal Header
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H1("AIFA Terminal Financiero", className="terminal-title"),
                    html.P("Análisis Financiero en Tiempo Real • Métricas de Rendimiento", className="terminal-subtitle")
                ], className="bloomberg-header-content")
            ])
        ], className="bloomberg-header mb-4"),
        
        # Trading Cards - Métricas Principales
        dbc.Row([
            dbc.Col([
                create_trading_card("Ingresos", "$290M MXN", "+5.4% vs mes anterior", "positive")
            ], width=3),
            dbc.Col([
                create_trading_card("Margen EBITDA", "29.3%", "+1.8% vs mes anterior", "positive") 
            ], width=3),
            dbc.Col([
                create_trading_card("ROI Anual", "22.1%", "+3.2% vs año anterior", "positive")
            ], width=3),
            dbc.Col([
                create_trading_card("Flujo Operativo", "$127M MXN", "+8.1% vs plan", "positive")
            ], width=3)
        ], className="trading-grid mb-4"),
        
        # KPI Grid Financiero
        dbc.Row([
            dbc.Col([create_financial_kpi("Ingresos por Pasajero", "$148", "+$12 vs objetivo", "mdi:account-cash")], width=3),
            dbc.Col([create_financial_kpi("Ingresos Aeronáuticos", "$89", "+$8 vs anterior", "mdi:airplane")], width=3),
            dbc.Col([create_financial_kpi("Ingresos No-Aeronáuticos", "$59", "+$4 vs anterior", "mdi:store")], width=3),
            dbc.Col([create_financial_kpi("% No-Aeronáuticos", "39.9%", "+2.1% vs plan", "mdi:percent")], width=3)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([create_financial_kpi("Costo por Operación", "$2,847", "-$156 optimización", "mdi:calculator")], width=3),
            dbc.Col([create_financial_kpi("Costo por Pasajero", "$42", "-$3 eficiencia", "mdi:wallet")], width=3),
            dbc.Col([create_financial_kpi("Costos Personal", "34.2%", "-1.8% del revenue", "mdi:account-group")], width=3),
            dbc.Col([create_financial_kpi("Margen Operativo", "18.7%", "+2.4% vs objetivo", "mdi:chart-line")], width=3)
        ], className="mb-4"),
        
        # Charts Grid 2x2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Análisis de Flujos de Ingresos", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="revenue-donut", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Estructura de Costos", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="cost-waterfall", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Rentabilidad vs Benchmarks", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="profitability-trends", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Análisis de Flujo de Efectivo", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="cashflow-analysis", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        # Financial Performance Matrix
        dbc.Card([
            dbc.CardHeader([
                html.H5("Matriz de Rendimiento Financiero", className="chart-title")
            ]),
            dbc.CardBody([
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Métrica"),
                            html.Th("Actual"),
                            html.Th("Objetivo"),
                            html.Th("Variación"),
                            html.Th("Tendencia"),
                            html.Th("Promedio Industria"),
                            html.Th("Rendimiento")
                        ])
                    ]),
                    html.Tbody([
                        create_financial_row("Ingresos por Pasajero", "$148", "$145", "+$3", "up", "$142", "excellent"),
                        create_financial_row("Margen EBITDA", "29.3%", "25.0%", "+4.3%", "up", "22.0%", "excellent"),
                        create_financial_row("Costo por Operación", "$2,847", "$3,000", "-$153", "down", "$3,200", "excellent"),
                        create_financial_row("% Ingresos No-Aero", "39.9%", "40.0%", "-0.1%", "stable", "35.0%", "good"),
                        create_financial_row("Margen Operativo", "18.7%", "16.0%", "+2.7%", "up", "15.0%", "excellent"),
                        create_financial_row("% Costos Personal", "34.2%", "35.0%", "-0.8%", "down", "38.0%", "good")
                    ])
                ], striped=True, hover=True, className="financial-table")
            ])
        ], className="financial-table-container")
    ])

def render_capacity_tab():
    """Renderiza el tab de capacidad operativa como centro de control aeroportuario avanzado"""
    return html.Div([
        # Operations Control Header
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H1("Centro de Control de Capacidad Operativa", className="section-title"),
                    html.P("Monitoreo en Tiempo Real • Utilización de Recursos • Optimización de Flujos", 
                           className="section-subtitle"),
                    html.Div([
                        dbc.Badge("OPERACIONAL", color="success", className="me-2"),
                        dbc.Badge("SISTEMA ACTIVO", color="info", className="me-2"),
                        dbc.Badge("99.7% UPTIME", color="warning", className="me-2"),
                        dbc.Badge("0 ALERTAS CRÍTICAS", color="success")
                    ], className="status-badges")
                ])
            ])
        ], className="operations-header mb-4"),
        
        # Gauges Grid - Visual KPIs
        dbc.Row([
            dbc.Col([
                create_capacity_gauge("Check-in", "98%", "245 m²", "2.1 m²/M pax", "mdi:check-circle", "success")
            ], width=4),
            dbc.Col([
                create_capacity_gauge("Salas Espera", "82%", "890 m²", "7.2 m²/M pax", "mdi:seat", "info")
            ], width=4),
            dbc.Col([
                create_capacity_gauge("Seguridad", "76%", "120 m²", "1.0 m²/M pax", "mdi:shield-check", "warning")
            ], width=4)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                create_capacity_gauge("Área Estéril", "85%", "450 m²", "3.8 m²/M pax", "mdi:lock", "success")
            ], width=4),
            dbc.Col([
                create_capacity_gauge("Equipajes", "80%", "2,400 bags/hr", "3,000 máx", "mdi:bag-suitcase", "info")
            ], width=4),
            dbc.Col([
                create_capacity_gauge("Puertas", "75%", "18/24 activas", "24 disponibles", "mdi:airplane-takeoff", "info")
            ], width=4)
        ], className="mb-4"),
        
        # Visual Analytics Grid
        dbc.Row([
            dbc.Col([
                # Heatmap de densidad
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Mapa de Calor - Densidad por Hora", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="capacity-heatmap", style={"height": "350px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                # Utilization trends
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Tendencias de Utilización", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="utilization-trends", style={"height": "350px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                # Capacity vs Demand
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Capacidad vs Demanda", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="capacity-demand", style={"height": "350px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                # Real-time monitor gauge
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Monitor General en Tiempo Real", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="general-gauge", style={"height": "350px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        # Live Operations Table
        dbc.Card([
            dbc.CardHeader([
                html.H5("Estado Operativo en Tiempo Real", className="chart-title"),
                html.Small("Actualización automática cada 30 segundos", className="text-muted")
            ]),
            dbc.CardBody([
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Zona/Sistema"),
                            html.Th("Capacidad"),
                            html.Th("Utilización"),
                            html.Th("Throughput"),
                            html.Th("Tiempo Espera"),
                            html.Th("Estado")
                        ])
                    ]),
                    html.Tbody([
                        create_status_row("Check-in Counters", "32/40", "98%", "180 pax/hr", "4.2 min", "optimal"),
                        create_status_row("Security Checkpoints", "8/10", "76%", "420 pax/hr", "8.1 min", "optimal"),
                        create_status_row("Immigration", "6/8", "68%", "380 pax/hr", "3.5 min", "optimal"),
                        create_status_row("Baggage Claim", "4/6", "85%", "2,400 bags/hr", "12.8 min", "warning"),
                        create_status_row("Gates", "18/24", "75%", "3,200 pax/hr", "N/A", "optimal"),
                        create_status_row("Parking", "2,847/3,500", "81%", "650 veh/hr", "N/A", "optimal")
                    ])
                ], striped=True, hover=True, className="operations-table")
            ])
        ], className="operations-table-container")
    ])

def render_security_tab():
    """Dashboard Bloomberg Terminal para Seguridad Operacional AIFA con 15 KPIs oficiales"""
    security_data = get_security_data()
    
    return html.Div([
        # Security Operations Header
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H1("Centro de Control de Seguridad Operacional", className="security-header-title"),
                    html.P("Monitoreo 15 KPIs Oficiales AIFA • Cumplimiento OACI • Gestión de Riesgos", 
                           className="security-header-subtitle"),
                    html.Div([
                        dbc.Badge("SMS ACTIVO", color="success", className="me-2"),
                        dbc.Badge("NIVEL SEGURIDAD A", color="info", className="me-2"), 
                        dbc.Badge("94.5/100 SCORE", color="warning", className="me-2"),
                        dbc.Badge("CUMPLIMIENTO OACI", color="success")
                    ], className="security-status-badges")
                ])
            ])
        ], className="security-operations-header mb-4"),
        
        # KPIs Principales (Top Row - 5 KPIs críticos)
        html.H5("KPIs Críticos de Seguridad", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                create_security_kpi_card(
                    "Incidentes en Pista",
                    security_data['runway_incidents']['rate'], 
                    security_data['runway_incidents']['unit'],
                    security_data['runway_incidents']['target'],
                    security_data['runway_incidents']['status'],
                    "mdi:runway"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Accidentes Mortales",
                    security_data['fatal_accidents']['rate'],
                    security_data['fatal_accidents']['unit'],
                    security_data['fatal_accidents']['target'],
                    security_data['fatal_accidents']['status'],
                    "mdi:alert-circle"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Accidentes Laborales",
                    security_data['work_accidents']['rate'],
                    security_data['work_accidents']['unit'],
                    security_data['work_accidents']['target'],
                    security_data['work_accidents']['status'],
                    "mdi:hard-hat"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Incursiones Pista",
                    security_data['runway_incursions']['rate'],
                    security_data['runway_incursions']['unit'],
                    security_data['runway_incursions']['target'],
                    security_data['runway_incursions']['status'],
                    "mdi:airplane-alert"
                )
            ], width=3, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Choques con Aves",
                    security_data['bird_strikes']['rate'],
                    security_data['bird_strikes']['unit'],
                    security_data['bird_strikes']['target'],
                    security_data['bird_strikes']['status'],
                    "mdi:bird"
                )
            ], width=3, className="mb-3")
        ]),
        
        # Centro de Control Visual
        html.H5("Centro de Control Visual", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Mapa Aeroportuario AIFA", className="chart-title")
                    ]),
                    dbc.CardBody([
                        create_airport_map_svg()
                    ])
                ], className="chart-card")
            ], width=8),
            
            dbc.Col([
                # Panel de incidentes tiempo real
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Incidentes Tiempo Real", className="chart-title")
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                DashIconify(icon="mdi:check-circle", width=24, height=24, style={"color": "#00ff88"}),
                                html.Span("Sin incidentes críticos", className="ms-2")
                            ], className="incident-row mb-2"),
                            html.Div([
                                DashIconify(icon="mdi:information", width=24, height=24, style={"color": "#00d4ff"}),
                                html.Span("FOD reportado Pista 12L", className="ms-2")
                            ], className="incident-row mb-2"),
                            html.Div([
                                DashIconify(icon="mdi:clock", width=24, height=24, style={"color": "#f59e0b"}),
                                html.Span("Inspección rutinaria 14:30", className="ms-2")
                            ], className="incident-row mb-2")
                        ])
                    ])
                ], className="chart-card"),
                
                # Estado sistemas críticos
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Sistemas Críticos", className="chart-title")
                    ]),
                    dbc.CardBody([
                        create_security_gauge("Iluminación", 99, 85, "mdi:lightbulb"),
                        create_security_gauge("Cámaras", 96, 80, "mdi:camera"),
                        create_security_gauge("Comunicaciones", 99, 90, "mdi:radio")
                    ])
                ], className="chart-card mt-3")
            ], width=4)
        ], className="mb-4"),
        
        # Dashboard Analítico (4 gráficos)
        html.H5("Análisis de Tendencias y Riesgos", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Tendencias Mensuales", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="security-trends-chart", style={"height": "320px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Comparativo vs Estándares OACI", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="security-standards-chart", style={"height": "320px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Matriz de Riesgos por Zona", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="security-risk-matrix", style={"height": "320px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Distribución de Tipos de Incidentes", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="security-incidents-distribution", style={"height": "320px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        # Métricas Operacionales (Grid de 10 KPIs restantes)
        html.H5("Métricas Operacionales Complementarias", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                create_security_kpi_card(
                    "Personal Seguridad",
                    security_data['security_staff']['rate'],
                    security_data['security_staff']['unit'],
                    security_data['security_staff']['target'],
                    security_data['security_staff']['status'],
                    "mdi:security"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Incidentes/Movimiento",
                    security_data['incident_movements']['rate'],
                    security_data['incident_movements']['unit'],
                    security_data['incident_movements']['target'],
                    security_data['incident_movements']['status'],
                    "mdi:airplane-settings"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Densidad Cámaras",
                    security_data['cameras_density']['rate'],
                    security_data['cameras_density']['unit'],
                    security_data['cameras_density']['target'],
                    security_data['cameras_density']['status'],
                    "mdi:camera-outline"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Eventos Fauna",
                    security_data['wildlife_events']['rate'],
                    security_data['wildlife_events']['unit'],
                    security_data['wildlife_events']['target'],
                    security_data['wildlife_events']['status'],
                    "mdi:paw"
                )
            ], width=3, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Luces Funcionales",
                    security_data['lighting_functional']['rate'],
                    security_data['lighting_functional']['unit'],
                    security_data['lighting_functional']['target'],
                    security_data['lighting_functional']['status'],
                    "mdi:lightbulb-on"
                )
            ], width=3, className="mb-3")
        ]),
        
        dbc.Row([
            dbc.Col([
                create_security_kpi_card(
                    "Incidentes Iluminación",
                    security_data['lighting_incidents']['rate'],
                    security_data['lighting_incidents']['unit'],
                    security_data['lighting_incidents']['target'],
                    security_data['lighting_incidents']['status'],
                    "mdi:lightbulb-alert"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Oquedades Atendidas",
                    security_data['pothole_attended']['rate'],
                    security_data['pothole_attended']['unit'],
                    security_data['pothole_attended']['target'],
                    security_data['pothole_attended']['status'],
                    "mdi:road-variant"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Mantenimiento Pistas",
                    security_data['runway_maintenance']['rate'],
                    security_data['runway_maintenance']['unit'],
                    security_data['runway_maintenance']['target'],
                    security_data['runway_maintenance']['status'],
                    "mdi:runway"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Reportes FOD",
                    security_data['fod_reports']['rate'],
                    security_data['fod_reports']['unit'],
                    security_data['fod_reports']['target'],
                    security_data['fod_reports']['status'],
                    "mdi:alert-box"
                )
            ], width=3, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Daños FOD",
                    security_data['fod_damage']['rate'],
                    security_data['fod_damage']['unit'],
                    security_data['fod_damage']['target'],
                    security_data['fod_damage']['status'],
                    "mdi:airplane-alert"
                )
            ], width=3, className="mb-3")
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

# Bloomberg Terminal Layout Helper
def get_bloomberg_layout():
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(10, 14, 39, 0.9)',
        'font': {'color': 'white', 'family': 'Inter'},
        'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40},
        'showlegend': True,
        'legend': {
            'font': {'color': 'white'},
            'bgcolor': 'rgba(26, 31, 58, 0.8)'
        },
        'xaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.1)'},
        'yaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.1)'}
    }

# Financial Charts Callbacks
@callback(Output('revenue-donut', 'figure'), Input('tabs', 'active_tab'))
def update_revenue_donut(active_tab):
    if active_tab != "financial":
        return {}
    
    return {
        'data': [go.Pie(
            labels=['Aeronáuticos', 'No-Aeronáuticos', 'Comerciales', 'Estacionamiento'],
            values=[178, 85, 19, 8],
            hole=0.6,
            marker_colors=['#00d4ff', '#00fff0', '#8b5cf6', '#ff6b35'],
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>$%{value}M MXN<br>%{percent}<extra></extra>'
        )],
        'layout': get_bloomberg_layout()
    }

@callback(Output('cost-waterfall', 'figure'), Input('tabs', 'active_tab'))
def update_cost_waterfall(active_tab):
    if active_tab != "financial":
        return {}
    
    return {
        'data': [go.Waterfall(
            name="Estructura de Costos",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Personal", "Mantenimiento", "Servicios", "Otros", "Total"],
            y=[78, 45, 32, 18, 173],
            text=['$78M', '$45M', '$32M', '$18M', '$173M'],
            textposition='outside',
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#ff4757"}},
            totals={"marker": {"color": "#00d4ff"}}
        )],
        'layout': get_bloomberg_layout()
    }

@callback(Output('profitability-trends', 'figure'), Input('tabs', 'active_tab'))
def update_profitability_trends(active_tab):
    if active_tab != "financial":
        return {}
    
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    return {
        'data': [
            go.Scatter(
                x=months,
                y=[15.2, 16.8, 17.5, 18.1, 18.7, 19.2, 18.9, 18.5, 19.1, 19.6, 19.8, 20.2],
                name='AIFA',
                mode='lines+markers',
                line=dict(color='#00d4ff', width=3),
                marker=dict(size=6, color='#00d4ff')
            ),
            go.Scatter(
                x=months,
                y=[14.5] * 12,
                name='Promedio Industria',
                mode='lines',
                line=dict(color='#ff6b35', width=2, dash='dash')
            ),
            go.Scatter(
                x=months,
                y=[16.0] * 12,
                name='Objetivo',
                mode='lines',
                line=dict(color='#00ff88', width=2, dash='dot')
            )
        ],
        'layout': get_bloomberg_layout()
    }

@callback(Output('cashflow-analysis', 'figure'), Input('tabs', 'active_tab'))
def update_cashflow_analysis(active_tab):
    if active_tab != "financial":
        return {}
    
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    return {
        'data': [
            go.Scatter(
                x=months,
                y=[85, 92, 98, 105, 112, 118, 125, 132, 127, 135, 142, 148],
                name='Flujo Operativo',
                mode='lines',
                fill='tonexty',
                line=dict(color='#00ff88'),
                fillcolor='rgba(0, 255, 136, 0.2)'
            ),
            go.Scatter(
                x=months,
                y=[78, 84, 89, 95, 101, 106, 112, 118, 115, 121, 127, 132],
                name='Flujo Libre',
                mode='lines',
                fill='tozeroy',
                line=dict(color='#00d4ff'),
                fillcolor='rgba(0, 212, 255, 0.2)'
            )
        ],
        'layout': get_bloomberg_layout()
    }

# Operations Center Layout Helper
def get_capacity_layout():
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(10, 14, 39, 0.9)',
        'font': {'color': 'white', 'family': 'Inter'},
        'margin': {'l': 60, 'r': 20, 't': 20, 'b': 60},
        'xaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.1)'},
        'yaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.1)'},
        'legend': {'font': {'color': 'white'}, 'bgcolor': 'rgba(26, 31, 58, 0.8)'}
    }

# Operations Center Charts Callbacks
@callback(Output('capacity-heatmap', 'figure'), Input('tabs', 'active_tab'))
def update_capacity_heatmap(active_tab):
    if active_tab != "capacity":
        return {}
    
    zones = ['Check-in', 'Seguridad', 'Inmigración', 'Espera', 'Gates', 'Equipajes']
    hours = ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
    
    density_matrix = [
        [20, 45, 60, 75, 85, 90, 80, 65, 40],  # Check-in
        [15, 40, 55, 70, 80, 85, 75, 60, 35],  # Seguridad
        [10, 35, 50, 65, 75, 80, 70, 55, 30],  # Inmigración
        [25, 50, 65, 80, 90, 95, 85, 70, 45],  # Espera
        [30, 55, 70, 85, 95, 100, 90, 75, 50], # Gates
        [18, 42, 58, 72, 82, 88, 78, 62, 38]   # Equipajes
    ]
    
    return {
        'data': [go.Heatmap(
            z=density_matrix, x=hours, y=zones,
            colorscale=[
                [0, '#0a0e27'], [0.2, '#1a1f3a'], [0.4, '#00d4ff'],
                [0.6, '#ffb627'], [0.8, '#ff6b35'], [1, '#ff4757']
            ],
            hovertemplate='<b>%{y}</b><br>Hora: %{x}<br>Densidad: %{z}%<extra></extra>'
        )],
        'layout': get_capacity_layout()
    }

@callback(Output('utilization-trends', 'figure'), Input('tabs', 'active_tab'))
def update_utilization_trends(active_tab):
    if active_tab != "capacity":
        return {}
    
    hours = list(range(6, 23))
    
    return {
        'data': [
            go.Scatter(x=hours, y=[20, 35, 55, 70, 80, 85, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40],
                      name='Check-in', line=dict(color='#00ff88', width=3)),
            go.Scatter(x=hours, y=[15, 30, 50, 65, 75, 80, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35],
                      name='Seguridad', line=dict(color='#ffb627', width=3)),
            go.Scatter(x=hours, y=[25, 40, 60, 75, 85, 90, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45],
                      name='Gates', line=dict(color='#8b5cf6', width=3)),
            go.Scatter(x=hours, y=[18, 33, 48, 63, 73, 78, 83, 78, 73, 68, 63, 58, 53, 48, 43, 38, 33],
                      name='Equipajes', line=dict(color='#ff6b35', width=3))
        ],
        'layout': get_capacity_layout()
    }

@callback(Output('capacity-demand', 'figure'), Input('tabs', 'active_tab'))
def update_capacity_demand(active_tab):
    if active_tab != "capacity":
        return {}
    
    hours = list(range(6, 23))
    
    return {
        'data': [
            go.Scatter(
                x=hours,
                y=[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                name='Capacidad Máxima',
                mode='lines',
                line=dict(color='#ff4757', width=2, dash='dash'),
                fill=None
            ),
            go.Scatter(
                x=hours,
                y=[20, 35, 55, 70, 80, 85, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40],
                name='Demanda Actual',
                mode='lines',
                line=dict(color='#00d4ff', width=3),
                fill='tonexty',
                fillcolor='rgba(0, 212, 255, 0.2)'
            )
        ],
        'layout': get_capacity_layout()
    }

@callback(Output('general-gauge', 'figure'), Input('tabs', 'active_tab'))
def update_general_gauge(active_tab):
    if active_tab != "capacity":
        return {}
    
    return {
        'data': [go.Indicator(
            mode="gauge+number+delta",
            value=78,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Utilización Terminal (%)"},
            delta={'reference': 75},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#00d4ff"},
                'steps': [
                    {'range': [0, 50], 'color': "rgba(0, 255, 136, 0.3)"},
                    {'range': [50, 80], 'color': "rgba(255, 182, 39, 0.3)"},
                    {'range': [80, 100], 'color': "rgba(255, 71, 87, 0.3)"}
                ],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 90}
            }
        )],
        'layout': get_capacity_layout()
    }

# Security Operations Charts Callbacks
@callback(Output('security-trends-chart', 'figure'), Input('tabs', 'active_tab'))
def update_security_trends(active_tab):
    if active_tab != "security":
        return {}
    
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    return {
        'data': [
            go.Scatter(x=months, y=[0.15, 0.12, 0.10, 0.08, 0.11, 0.09, 0.12, 0.10, 0.13, 0.11, 0.12, 0.12],
                      name='Incidentes Pista', line=dict(color='#ff4757', width=3),
                      hovertemplate='<b>Incidentes Pista</b><br>%{x}: %{y}/1000 ops<extra></extra>'),
            go.Scatter(x=months, y=[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                      name='Accidentes Mortales', line=dict(color='#00ff88', width=3),
                      hovertemplate='<b>Accidentes Mortales</b><br>%{x}: %{y}/1000 ops<extra></extra>'),
            go.Scatter(x=months, y=[0.90, 0.85, 0.88, 0.82, 0.87, 0.91, 0.86, 0.89, 0.85, 0.83, 0.85, 0.85],
                      name='Choques Aves', line=dict(color='#f59e0b', width=3),
                      hovertemplate='<b>Choques Aves</b><br>%{x}: %{y}/1000 ops<extra></extra>'),
            go.Scatter(x=months, y=[0.08, 0.06, 0.04, 0.03, 0.05, 0.04, 0.06, 0.05, 0.07, 0.05, 0.05, 0.05],
                      name='Incursiones Pista', line=dict(color='#00d4ff', width=3),
                      hovertemplate='<b>Incursiones Pista</b><br>%{x}: %{y}/1000 ops<extra></extra>')
        ],
        'layout': get_security_chart_layout()
    }

@callback(Output('security-standards-chart', 'figure'), Input('tabs', 'active_tab'))
def update_security_standards(active_tab):
    if active_tab != "security":
        return {}
    
    kpis = ['Incidentes\nPista', 'Accidentes\nMortales', 'Choques\nAves', 'Incursiones\nPista', 'Personal\nSeguridad']
    aifa_values = [0.12, 0.00, 0.85, 0.05, 45]
    oaci_standards = [0.15, 0.00, 1.20, 0.10, 40]
    
    return {
        'data': [
            go.Bar(x=kpis, y=aifa_values, name='AIFA Actual',
                   marker=dict(color='#00d4ff', opacity=0.8),
                   hovertemplate='<b>AIFA</b><br>%{x}: %{y}<extra></extra>'),
            go.Bar(x=kpis, y=oaci_standards, name='Estándar OACI',
                   marker=dict(color='#f59e0b', opacity=0.6),
                   hovertemplate='<b>OACI</b><br>%{x}: %{y}<extra></extra>')
        ],
        'layout': get_security_chart_layout()
    }

@callback(Output('security-risk-matrix', 'figure'), Input('tabs', 'active_tab'))
def update_security_risk_matrix(active_tab):
    if active_tab != "security":
        return {}
    
    zones = ['Terminal', 'Pista 12L', 'Pista 12R', 'Torre Control', 'Área Carga', 'Estacionamiento']
    risk_factors = ['FOD', 'Fauna', 'Clima', 'Humano', 'Equipo']
    
    risk_matrix = [
        [2, 1, 3, 2, 1, 2],  # FOD
        [1, 3, 3, 1, 2, 1],  # Fauna
        [2, 3, 3, 2, 2, 1],  # Clima
        [3, 2, 2, 2, 3, 2],  # Humano
        [2, 2, 2, 3, 2, 1]   # Equipo
    ]
    
    return {
        'data': [go.Heatmap(
            z=risk_matrix, x=zones, y=risk_factors,
            colorscale=[
                [0, '#00ff88'], [0.33, '#f59e0b'], [0.66, '#ff6b35'], [1, '#ff4757']
            ],
            hovertemplate='<b>%{y} - %{x}</b><br>Nivel Riesgo: %{z}<extra></extra>',
            showscale=True,
            colorbar=dict(
                title="Nivel Riesgo",
                titleside="right",
                tickmode="array",
                tickvals=[1, 2, 3],
                ticktext=["Bajo", "Medio", "Alto"],
                len=0.6
            )
        )],
        'layout': get_security_chart_layout()
    }

@callback(Output('security-incidents-distribution', 'figure'), Input('tabs', 'active_tab'))
def update_security_incidents_distribution(active_tab):
    if active_tab != "security":
        return {}
    
    incident_types = ['FOD', 'Fauna', 'Incursiones', 'Mantenimiento', 'Iluminación', 'Otros']
    values = [25, 20, 15, 18, 12, 10]
    colors = ['#ff4757', '#f59e0b', '#ff6b35', '#00d4ff', '#8b5cf6', '#00ff88']
    
    return {
        'data': [go.Pie(
            labels=incident_types,
            values=values,
            hole=0.4,
            marker=dict(colors=colors, line=dict(color='#0a0e27', width=2)),
            hovertemplate='<b>%{label}</b><br>Incidentes: %{value}<br>Porcentaje: %{percent}<extra></extra>',
            textinfo='label+percent',
            textposition='outside'
        )],
        'layout': {
            **get_security_chart_layout(),
            'showlegend': False,
            'margin': dict(l=20, r=20, t=20, b=20)
        }
    }

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