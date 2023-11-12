# pages/home.py

import dash
from dash import dcc, html

# Define the layout for the home page
home_layout = html.Div([
    html.H1("Welcome to the Home Page"),
    dcc.Link("Go to Weights Page", href="/weight"),
])
