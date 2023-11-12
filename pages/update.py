# pages/update.py

import dash
from dash import dcc, html, Input, Output
import pandas as pd
from dash.dependencies import Input, Output, State
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongodb_connection_string = os.getenv("MONGODB_CONNECTION_STRING")

if not mongodb_connection_string:
    raise ValueError("MongoDB connection string not set in environment variable.")

# Read the CSV data
df = pd.read_csv("data/weights.csv")

# Define the layout for the update page
update_layout = html.Div([
    html.H1("Update Weight"),
    dcc.Input(id="weight-input", type="number", placeholder="Enter weight (int or float)"),
    html.Button("Submit", id="submit-button"),
    html.Div(id="update-status"),
])

# Define a callback to update the CSV file
def update_csv(weight_value):
    mongo_client = MongoClient(mongodb_connection_string)
    db = mongo_client["gym"]
    collection = db["weight"]

    global df  # Declare df as a global variable
    try:
        weight = float(weight_value)
        today_date = datetime.now().strftime("%Y-%m-%d")
        new_data = pd.DataFrame({"date": [today_date], "weights": [weight]})
        
        # Update CSV
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv("data/weights.csv", index=False)

        # Update MongoDB
        data_to_insert = {"date": today_date, "weight": weight}
        collection.insert_one(data_to_insert)
        
        return f"Weight {weight} added successfully on {today_date}."
    except ValueError:
        return "Invalid input. Please enter a valid number."




        return f"Weight {weight} added successfully on {today_date}."
    except ValueError:
        return "Invalid input. Please enter a valid number."

# Create a callback to handle updates
def update_weight_on_submit(n_clicks, weight_value):
    if n_clicks is None:
        return ""
    else:
        update_result = update_csv(weight_value)
        return update_result

# Define the callback for updating the CSV file
def update_weight_callback(app):
    @app.callback(
        Output("update-status", "children"),
        Input("submit-button", "n_clicks"),
        State("weight-input", "value"),
    )
    def update_weight(n_clicks, weight_value):
        return update_weight_on_submit(n_clicks, weight_value)

# Define a function to create the update page with the app context
def create_update_page(app):
    update_weight_callback(app)
    return update_layout
