import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from ..data.simulated_data import generate_route_data, generate_state_penetration

# Generate data
route_data = generate_route_data()
state_data = generate_state_penetration()

layout = html.Div([
    # World Route Map
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Red de Rutas Internacionales AIFA", className="chart-title"),
                    html.Small("Conexiones actuales y tráfico de pasajeros", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    dcc.Graph(id="world-routes-map")
                ])
            ], className="chart-card")
        ], width=12)
    ], className="mb-4"),
    
    # Mexico Penetration Map and Route Performance
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Penetración por Estados", className="chart-title"),
                    html.Small("Participación de mercado nacional", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    dcc.Graph(id="mexico-penetration-map")
                ])
            ], className="chart-card")
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Top Destinos", className="chart-title"),
                    html.Small("Por volumen de pasajeros", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    html.Div(id="top-destinations-list")
                ])
            ], className="chart-card")
        ], width=4)
    ], className="mb-4"),
    
    # Route Performance Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Factor de Carga por Ruta", className="chart-title"),
                    html.Small("Eficiencia operativa", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    dcc.Graph(id="load-factor-chart")
                ])
            ], className="chart-card")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Frecuencias vs Pasajeros", className="chart-title"),
                    html.Small("Optimización de rutas", className="chart-subtitle")
                ]),
                dbc.CardBody([
                    dcc.Graph(id="frequency-passengers-chart")
                ])
            ], className="chart-card")
        ], width=6)
    ])
])

# Callbacks
@callback(
    Output('world-routes-map', 'figure'),
    Input('world-routes-map', 'id')
)
def update_world_routes(_):
    fig = go.Figure()
    
    # Add route lines
    for _, route in route_data.iterrows():
        fig.add_trace(go.Scattergeo(
            lon=[route['origin_lon'], route['lon']],
            lat=[route['origin_lat'], route['lat']],
            mode='lines',
            line=dict(width=2, color='#00d4ff'),
            opacity=0.6,
            showlegend=False
        ))
    
    # Add AIFA marker
    fig.add_trace(go.Scattergeo(
        lon=[route_data['origin_lon'].iloc[0]],
        lat=[route_data['origin_lat'].iloc[0]],
        text=['AIFA'],
        mode='markers+text',
        marker=dict(size=15, color='#f59e0b', symbol='airport'),
        textposition='top center',
        name='AIFA',
        showlegend=False
    ))
    
    # Add destination markers
    fig.add_trace(go.Scattergeo(
        lon=route_data['lon'],
        lat=route_data['lat'],
        text=route_data['city'],
        mode='markers+text',
        marker=dict(
            size=route_data['passengers']/5000,
            color=route_data['load_factor'],
            colorscale='Viridis',
            colorbar=dict(title="Factor de Carga (%)")
        ),
        textposition='top center',
        name='Destinos',
        showlegend=False
    ))
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular',
            bgcolor='rgba(0,0,0,0)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

@callback(
    Output('mexico-penetration-map', 'figure'),
    Input('mexico-penetration-map', 'id')
)
def update_mexico_penetration(_):
    # Mexico states geojson simplified
    fig = go.Figure()
    
    # Create a bar chart instead of choropleth for simplicity
    fig.add_trace(go.Bar(
        x=state_data['state'],
        y=state_data['penetration'],
        marker_color='#00d4ff',
        text=state_data['penetration'].round(1),
        textposition='auto'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title='Estado',
            tickangle=45
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title='Penetración (%)'
        ),
        margin=dict(l=20, r=20, t=20, b=80)
    )
    
    return fig

@callback(
    Output('top-destinations-list', 'children'),
    Input('top-destinations-list', 'id')
)
def update_top_destinations(_):
    sorted_routes = route_data.sort_values('passengers', ascending=False).head(8)
    
    destinations = []
    for _, route in sorted_routes.iterrows():
        destinations.append(
            html.Div([
                html.Div([
                    html.Div([
                        html.Strong(route['city']),
                        html.Br(),
                        html.Small(route['country'], style={'color': '#8b92a9'})
                    ], className="destination-info"),
                    html.Div([
                        html.Div(f"{route['passengers']:,}", className="metric-value"),
                        html.Small("pasajeros", className="metric-label")
                    ], className="destination-metric")
                ], className="destination-row"),
                html.Div([
                    html.Small(f"Factor de carga: {route['load_factor']:.1f}%", 
                              style={'color': '#00d4ff'}),
                    html.Br(),
                    html.Small(f"Frecuencia: {route['frequency']} vuelos/mes",
                              style={'color': '#8b92a9'})
                ], className="destination-details")
            ], className="destination-item")
        )
    
    return destinations

@callback(
    Output('load-factor-chart', 'figure'),
    Input('load-factor-chart', 'id')
)
def update_load_factor(_):
    sorted_routes = route_data.sort_values('load_factor', ascending=True)
    
    colors = ['#ff4757' if x < 80 else '#f59e0b' if x < 85 else '#00ff88' for x in sorted_routes['load_factor']]
    
    fig = go.Figure(go.Bar(
        x=sorted_routes['load_factor'],
        y=sorted_routes['city'],
        orientation='h',
        marker_color=colors,
        text=sorted_routes['load_factor'].round(1),
        textposition='auto'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title='Factor de Carga (%)'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)'
        ),
        margin=dict(l=80, r=20, t=20, b=20)
    )
    
    return fig

@callback(
    Output('frequency-passengers-chart', 'figure'),
    Input('frequency-passengers-chart', 'id')
)
def update_frequency_passengers(_):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=route_data['frequency'],
        y=route_data['passengers'],
        mode='markers+text',
        text=route_data['city'],
        textposition='top center',
        marker=dict(
            size=route_data['load_factor']/3,
            color=route_data['load_factor'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Factor de Carga (%)")
        ),
        name='Rutas'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title='Frecuencia (vuelos/mes)'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title='Pasajeros Mensuales'
        ),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    return fig