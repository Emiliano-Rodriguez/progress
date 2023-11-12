from datetime import datetime, timedelta  # Updated import
import plotly.graph_objs as go
import numpy as np
import dash
from dash import dcc, html, Input, Output


def create_heatmap_page(app):
    weights_layout = html.Div(
        [
            dcc.Graph(
                id="map-chart",
                config={"displayModeBar": False},
                figure={},  # Initialize with an empty figure
                style={"width": "80%", "position": "absolute", "left": "10%"},
            ),
            dcc.Interval(
                id="graph-interval",
                interval=10 * 1000,  # Refresh every 10 seconds (adjust as needed)
                n_intervals=0,
            ),
        ]
    )

    @app.callback(
        Output("map-chart", "figure"), [Input("graph-interval", "n_intervals")]
    )
    def holidays(n):
        year = datetime.now().year
        d1 = datetime(year, 1, 1)
        d2 = datetime(year, 12, 31)
        delta = d2 - d1
        dates_in_year = [d1 + timedelta(i) for i in range(delta.days + 1)]
        weekdays_in_year = [i.weekday() for i in dates_in_year]
        weeknumber_of_dates = [int(i.strftime("%V")) for i in dates_in_year]
        z = np.random.uniform(low=0.0, high=1.0, size=(len(dates_in_year),))
        text = [str(i) for i in dates_in_year]
        colorscale=[[False, "#eeeeee"], [True, "#76cf63"]]


        data = [
            go.Heatmap(
                x=weeknumber_of_dates,
                y=weekdays_in_year,
                z=z,
                text=text,
                hoverinfo="text",
                xgap=3,
                ygap=3,
                showscale=False,
                colorscale=colorscale
            )
        ]
        layout = go.Layout(
            title="Calendar",
            height=280,

            yaxis=dict(
                showline=False, showgrid=False,zeroline=False,
                tickmode="array",
                ticktext=["Mon", "Tues", "Ons", "Tors", "Fre", "Lør", "Søn"],
                tickvals=[0, 1, 2, 3, 4, 5, 6],
            ),
            xaxis=dict(
                showline = False, showgrid = False, zeroline = False,
                title="Ugedag",
            ),
            font={"size":10, "color":"#9e9e9e"},
            plot_bgcolor=("#fff"),
            margin = dict(t=40),
        )







        fig = go.Figure(data=data, layout=layout)
        return fig

    return weights_layout
