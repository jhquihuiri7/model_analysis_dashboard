# Dash imports
from dash import Dash, dcc, html, Input, Output, _dash_renderer

# Backend imports
from backend.data_setup import setup_data

# External libraries
import plotly.graph_objects as go
import dash_mantine_components as dmc
_dash_renderer._set_react_version("18.2.0")

# Components
from components.graph_components import main_graph, spread_graph
from components.table_components import main_table

# Initialize the Dash app
external_stylesheets = [
    dmc.styles.NOTIFICATIONS,
    dmc.styles.ALL
]

external_scripts = [
    "https://cdn.tailwindcss.com"
]

client =  setup_data()


app = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Model Anlalysis Dashboard"

# Define the app layout
app.layout = dmc.MantineProvider(
    html.Div(
        className="p-10 w-full",
        children=[
            html.H1("How Shocky will NYIS be?", className="text-2xl font-bold"),
            dcc.Graph(id="main_graph", figure=main_graph(client, "NYISpjm shock X forecast", "NYIS pjm DA regular prediction", "NYIS pjm DA")),
            main_table(client,["NYISpjm shock X forecast","NYIS pjm DA regular prediction"]),
            html.H1("How Shocky will PJM be?", className="text-2xl font-bold"),
            dcc.Graph(id="main_graph2", figure=main_graph(client, "PJMnyis shock X forecast", "PJM nyis DA regular prediction", "PJM nyis DA")),
            main_table(client,["NYISpjm shock X forecast","NYIS pjm DA regular prediction"]),
            html.H1("PJM to NYIS Shock models predicted spread", className="text-2xl font-bold"),
            dcc.Graph(id="main_graph_2", figure=spread_graph(client)),
        ],
    )
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
