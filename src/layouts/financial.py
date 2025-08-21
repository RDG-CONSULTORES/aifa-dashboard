import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from ..data.simulated_data import generate_financial_data

# Generate data
financial_data = generate_financial_data()

layout = html.Div([
    html.H4("Análisis Financiero", className="page-title"),
    html.P("Performance financiero y rentabilidad", className="page-subtitle"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Evolución de Ingresos", className="chart-title"),
                    html.Small("Millones MXN", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    dcc.Graph(id="revenue-trend")
                ])
            ], className="chart-card")
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Margen EBITDA", className="chart-title"),
                    html.Small("Rentabilidad operativa", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    dcc.Graph(id="ebitda-margin")
                ])
            ], className="chart-card")
        ], width=4)
    ])
])

@callback(
    Output('revenue-trend', 'figure'),
    Input('revenue-trend', 'id')
)
def update_revenue_trend(_):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=financial_data['month'],
        y=financial_data['revenue'],
        name='Ingresos',
        marker_color='#00d4ff'
    ))
    
    fig.add_trace(go.Bar(
        x=financial_data['month'],
        y=financial_data['costs'],
        name='Costos',
        marker_color='#ff4757'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Millones MXN'),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    return fig

@callback(
    Output('ebitda-margin', 'figure'),
    Input('ebitda-margin', 'id')
)
def update_ebitda_margin(_):
    current_margin = financial_data['margin'].iloc[-1]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_margin,
        title={'text': "Margen EBITDA (%)"},
        gauge={
            'axis': {'range': [None, 50]},
            'bar': {'color': "#00d4ff"},
            'steps': [
                {'range': [0, 15], 'color': "rgba(255,71,87,0.3)"},
                {'range': [15, 25], 'color': "rgba(245,158,11,0.3)"},
                {'range': [25, 50], 'color': "rgba(0,255,136,0.3)"}
            ]
        }
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig