# Dash imports: Essential components for creating the Dash web application
from dash import Dash, dcc, html, Input, Output, _dash_renderer

# Backend imports: Data setup logic from the backend module
from backend.data_setup import setup_data

# External libraries: Libraries for data visualization (Plotly) and handling data (pandas)
import plotly.graph_objects as go
import pandas as pd
import dash_mantine_components as dmc

# Setting the React version used by Dash
_dash_renderer._set_react_version("18.2.0")

# Components: Import custom components for graphs, tables, and buttons
from components.graph_components import main_graph, spread_graph
from components.table_components import main_table
from components.button_components import last_day_toggle

# Initialize the Dash app
external_stylesheets = [
    dmc.styles.NOTIFICATIONS,  # Mantine notification styles
    dmc.styles.ALL  # All Mantine component styles
]

external_scripts = [
    "https://cdn.tailwindcss.com"  # Tailwind CSS for utility-first styling
]

# Set up the data by calling the setup_data function
client =  setup_data()

# Initialize the Dash web application
app = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],  # Responsive design
)

# Set the title for the web app
app.title = "Model Analysis Dashboard"

# Define the layout of the Dash application
app.layout = dmc.MantineProvider(
    html.Div(
        className="p-10 w-full",  # Padding and width settings for the layout
        children=[
            # Toggle switch to show/hide last day's data
            last_day_toggle(),
            
            # Heading for the first graph
            html.H1("How Shocky will NYIS be?", className="text-2xl font-bold"),
            
            # Graph displaying the shock prediction for NYIS
            dcc.Graph(id="main_graph", figure=main_graph(client.df, "NYISpjm shock X forecast", "NYIS pjm DA regular prediction", "NYIS pjm DA")),
            
            # Table displaying the data for the first model
            main_table(pd.DataFrame(),["NYISpjm shock X forecast","NYIS pjm DA regular prediction"],"main_table"),
            
            # Heading for the second graph
            html.H1("How Shocky will PJM be?", className="text-2xl font-bold"),
            
            # Graph displaying the shock prediction for PJM
            dcc.Graph(id="main_graph2", figure=main_graph(client.df, "PJMnyis shock X forecast", "PJM nyis DA regular prediction", "PJM nyis DA")),
            
            # Table displaying the data for the second model
            main_table(pd.DataFrame(),["NYISpjm shock X forecast","NYIS pjm DA regular prediction"], "main_table2"),
            
            # Heading for the spread graph
            html.H1("PJM to NYIS Shock models predicted spread", className="text-2xl font-bold"),
            
            # Graph displaying the spread between PJM and NYIS shock models
            dcc.Graph(id="spread_graph", figure=spread_graph(client.df, "PJM to NYIS shock spread")),
        ],
    )
)

# Define the callback function to update the components based on input
@app.callback(
    [Output("main_graph", "figure"),
     Output("main_graph2", "figure"), 
     Output("spread_graph", "figure"),
     Output("main_table", "children"),
     Output("main_table2", "children")],
    [Input("last_day_toggle", "value")],  # Input is the value of the last_day_toggle (whether it's on or off)
)
def update_dashboard(last_day_toggle):
    # Access the data from the client
    df = client.df
    table_df = pd.DataFrame()  # Initialize an empty DataFrame for table data
    display = False  # Initially, do not display the table

    # If the toggle is on, filter the data to only show the last day's data
    if last_day_toggle:
        last_day = client.df.index.max().date()  # Get the most recent date
        table_df = df = client.df[client.df.index.date == last_day]  # Filter data for the last day
        display = True  # Set display to True to show the table
        
    # Create the graphs with the updated data
    graph1 = main_graph(df, "NYISpjm shock X forecast", "NYIS pjm DA regular prediction", "NYIS pjm DA") 
    graph2 = main_graph(df, "PJMnyis shock X forecast", "PJM nyis DA regular prediction", "PJM nyis DA")
    graphS = spread_graph(df, "PJM to NYIS shock spread")
    
    # Create the tables with the updated data
    table1 = main_table(table_df, ["NYISpjm shock X forecast", "NYIS pjm DA regular prediction"], "main_table", display)
    table2 = main_table(table_df, ["NYISpjm shock X forecast", "NYIS pjm DA regular prediction"], "main_table2", display)

    # Return the updated figures and table components
    return graph1, graph2, graphS, table1, table2

# Run the Dash application
if __name__ == "__main__":
    app.run_server(debug=True)
