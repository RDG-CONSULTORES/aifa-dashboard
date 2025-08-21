import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

layout = html.Div([
    html.H4("Seguridad", className="page-title"),
    html.P("Métricas de seguridad operacional y compliance", className="page-subtitle"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("En desarrollo", style={'color': '#8b92a9', 'textAlign': 'center', 'marginTop': '50px'})
                ])
            ], className="chart-card")
        ], width=12)
    ])
])