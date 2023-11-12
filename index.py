# index.py

import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from pages import home, weight, update  # Import the home and weights pages
from pymongo import MongoClient

# Initialize the Dash app with Bootstrap styles
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

# Define the layout for the home page
home_layout = home.home_layout

# Define the layout for the weights page
weights_layout = weight.create_weights_page()  # Call the function without arguments

# Define the layout for the update page
update_layout = update.create_update_page(app)

# Define the app layout with a Bootstrap dropdown menu
app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),
    dbc.Row([
        dbc.Col([
            dbc.DropdownMenu(
                label="Navigate",
                children=[
                    dbc.DropdownMenuItem("Home", href="/"),
                    dbc.DropdownMenuItem("Weight", href="/weight"),
                    dbc.DropdownMenuItem("Update", href="/update"), 
                ],
            ),
            html.Div(id="page-content")
        ], width={"size": 6, "offset": 3}),
    ]),
])

# Define callback to update the page content based on the URL
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/weight":
        return weights_layout  # Display the weights page
    elif pathname == "/update":
        return update_layout  # Display the update page
    else:
        return home_layout  # Display the home page

if __name__ == "__main__":
    app.run_server(debug=True)
