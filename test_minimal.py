#!/usr/bin/env python3
"""Minimal test to verify tab functionality"""

from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Tabs([
        dbc.Tab(label="Test 1", tab_id="test1"),
        dbc.Tab(label="Test 2", tab_id="test2"),
        dbc.Tab(label="Capacity", tab_id="capacity"),
    ], id="tabs", active_tab="test1"),
    
    html.Div(id="tab-content")
])

@callback(Output("tab-content", "children"),
          Input("tabs", "active_tab"))
def render_content(active_tab):
    if active_tab == "test1":
        return html.Div("Test 1 content works!")
    elif active_tab == "test2":
        return html.Div("Test 2 content works!")
    elif active_tab == "capacity":
        return html.Div([
            html.H4("Capacity Tab Works!"),
            html.P("This is the capacity tab content.")
        ])
    else:
        return html.Div(f"Unknown tab: {active_tab}")

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)