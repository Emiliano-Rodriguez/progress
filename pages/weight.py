# pages/weights.py

from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
from pymongo import MongoClient
import os
from dotenv import load_dotenv


mongodb_connection_string = os.getenv("MONGODB_CONNECTION_STRING")

# Define the layout for the weights page
def create_weights_page():
    # Read the CSV data
    df = pd.read_csv("data/weights.csv")
    mongo_client = MongoClient(mongodb_connection_string)
    db = mongo_client["gym"]
    collection = db["weight"]

    cursor = collection.find()
    mongo_data = list(cursor)
    df = pd.DataFrame(mongo_data)




    weights_layout = html.Div([
        dcc.Graph(
            id="weights-chart",
            config={"displayModeBar": False},
            figure={
                "data": [
                    go.Scatter(
                        x=df["date"],
                        y=df["weight"],
                        mode="lines",
                        marker={"color": "blue"},
                    )
                ],
                "layout": go.Layout(
                    title="Weight Data",
                    xaxis={"title": "Date"},
                    yaxis={"title": "Weight"},
                ),
            },
            style={"width": "100%", "position": "absolute", "left": "-1%"},
        ),
        dcc.Interval(
            id="graph-interval",
            interval=5 * 1000,  # Refresh every 60 seconds (adjust as needed)
            n_intervals=0,
        ),

    ])

    return weights_layout