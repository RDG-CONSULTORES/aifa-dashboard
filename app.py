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

# Import layouts
from src.layouts import strategic, geographic, capacity, security, quality, productivity, financial
from src.data.simulated_data import generate_kpi_data, generate_route_data, generate_financial_data

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.Div([
                DashIconify(icon="fluent:airplane-take-off-20-filled", width=40, height=40, style={'color': '#00d4ff'}),
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
                dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0)  # Update every 30 seconds
            ], className="header-right")
        ], className="header-container")
    ], className="header"),
    
    # Navigation tabs
    dbc.Tabs([
        dbc.Tab(label="KPIs Estratégicos", tab_id="strategic", 
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
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Análisis Financiero", tab_id="financial",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Análisis Geográfico", tab_id="geographic",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'})
    ], id="tabs", active_tab="strategic", className="nav-tabs"),
    
    # Tab content
    html.Div(id="tab-content", className="content-area"),
    
    # Add CSS link
    html.Link(rel='stylesheet', href='/assets/style.css')
])

# Callback for tab content
@callback(Output("tab-content", "children"),
          Input("tabs", "active_tab"))
def render_tab_content(active_tab):
    if active_tab == "strategic":
        return strategic.layout
    elif active_tab == "geographic":
        return geographic.layout
    elif active_tab == "capacity":
        return capacity.layout
    elif active_tab == "security":
        return security.layout
    elif active_tab == "quality":
        return quality.layout
    elif active_tab == "productivity":
        return productivity.layout
    elif active_tab == "financial":
        return financial.layout
    return html.Div()

# Callback for live time update
@callback(Output('live-update-time', 'children'),
          Input('interval-component', 'n_intervals'))
def update_time(n):
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)