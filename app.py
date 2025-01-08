import io

# Dash imports: Essential components for creating the Dash web application
from dash import Dash, dcc, html, Input, Output, _dash_renderer, callback_context, State, exceptions


# Backend imports: Data setup logic from the backend module
from backend.data_setup import setup_data
import utils.export_variables as variables
from utils.logic_functions import parse_table_data

# External libraries: Libraries for data visualization (Plotly) and handling data (pandas)
import plotly.graph_objects as go
import pandas as pd
import dash_mantine_components as dmc

# Setting the React version used by Dash
_dash_renderer._set_react_version("18.2.0")

# Components: Import custom components for graphs, tables, and buttons
from components.graph_components import main_graph, spread_graph
from components.table_components import main_table
from components.button_components import last_day_toggle, table_slider

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
            
            table_slider("main_table_slider","download_button"),
            
            # Table displaying the data for the first model
            html.Div(
                main_table(pd.DataFrame(),["NYISpjm shock X forecast","NYIS pjm DA regular prediction"],"main_table"),
                id="main_table"
            ),
            
            # Heading for the second graph
            html.H1("How Shocky will PJM be?", className="text-2xl font-bold"),
            
            # Graph displaying the shock prediction for PJM
            dcc.Graph(id="main_graph2", figure=main_graph(client.df, "PJMnyis shock X forecast", "PJM nyis DA regular prediction", "PJM nyis DA")),
            
            table_slider("main_table2_slider","download_button2"),
            
            # Table displaying the data for the second model
            html.Div(
                main_table(pd.DataFrame(),["PJMnyis shock X forecast", "PJM nyis DA regular prediction"], "main_table2"),
                id="main_table2"
            ),
            
            # Heading for the spread graph
            html.H1("PJM to NYIS Shock models predicted spread", className="text-2xl font-bold"),
            
            # Graph displaying the spread between PJM and NYIS shock models
            dcc.Graph(id="spread_graph", figure=spread_graph(client.df, "PJM to NYIS shock spread")),
            
            # Heading for the spread graph
            html.H1("NYIS to PJM Shock models predicted spread", className="text-2xl font-bold"),
            
            # Graph displaying the spread between PJM and NYIS shock models
            dcc.Graph(id="spread_graph2", figure=spread_graph(client.df, "NYIS to PJM shock spread")),
            
            dcc.Download(id="download-data")
        ]
    )
)

@app.callback(
    Output("download-data", "data", allow_duplicate=True),
    Input("download_button", "n_clicks"),
    Input("download_button2", "n_clicks"),
    State("main_table_data", "rowData"),
    State("main_table2_data", "rowData"),
    prevent_initial_call=True
)
def download_logic(download_button, download_button2, main_table_data, main_table2_data):
    ctx = callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    
    buffer = io.StringIO()
    export_df = pd.DataFrame()
    if triggered_id == "download_button":
        export_df = parse_table_data(main_table_data, variables.export_df1.index)
    else:
        export_df = parse_table_data(main_table2_data, variables.export_df2.index)
        
    export_df.to_csv(buffer, index=False, encoding="utf-8")
    buffer.seek(0)
    
    return dict(content=buffer.getvalue(), filename="data.csv")

# Define the callback function to update the components based on input
@app.callback(
    [Output("main_graph", "figure"),
     Output("main_graph2", "figure"), 
     Output("spread_graph", "figure"),
     Output("spread_graph2", "figure"),
     Output("main_table", "children"),
     Output("main_table2", "children"),
     Output("main_table_slider_container", "className"),
     Output("main_table2_slider_container", "className")],
    [Input("last_day_toggle", "value"),
     Input("main_table_slider","value"),
     Input("main_table2_slider","value"),
     Input("main_table_data", "cellValueChanged"),
     Input("main_table2_data", "cellValueChanged")],
    [State("main_table_data", "rowData"),
     State("main_table2_data", "rowData"),
     State("main_table", "children"),
     State("main_table2", "children")],
)
def update_dashboard(last_day_toggle, main_table_slider, main_table2_slider, main_table_data, main_table2_data,main_table_data_state, main_table2_data_state, main_table_state, main_table2_state):
    
    ctx = callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    
    # Access the data from the client
    df = client.df
    table_df = pd.DataFrame()  # Initialize an empty DataFrame for table data
    display = False  # Initially, do not display the table
    

    # If the toggle is on, filter the data to only show the last day's data
    if last_day_toggle:
        last_day = client.df.index.max().date()  # Get the most recent date
        table_df = df = client.df[client.df.index.date == last_day]  # Filter data for the last day
        display = True  # Set display to True to show the table
    
    slider_className="inline mt-5 w-full" if display else "hidden mt-5 w-full"
      
    # Create the graphs with the updated data
    graph1 = main_graph(df, "NYISpjm shock X forecast", "NYIS pjm DA regular prediction", "NYIS pjm DA", display, main_table_slider) 
    graph2 = main_graph(df, "PJMnyis shock X forecast", "PJM nyis DA regular prediction", "PJM nyis DA", display, main_table2_slider)
    graphS = spread_graph(df, "PJM to NYIS shock spread")
    graphS2 = spread_graph(df, "NYIS to PJM shock spread")
    
    # Create the tables with the updated data
    table1 = main_table(table_df, ["NYISpjm shock X forecast", "NYIS pjm DA regular prediction"], "main_table",display, main_table_slider)
    table2 = main_table(table_df, ["PJMnyis shock X forecast", "PJM nyis DA regular prediction"], "main_table2",display, main_table2_slider)
    

    if triggered_id == "main_table_data":
        try:
            export_df = parse_table_data(main_table_data_state, df.index)
            if not export_df.empty:
                export_df.set_index('Datetime (HB)', inplace=True)
                export_df["NYIS pjm DA"] = df["NYIS pjm DA"]
                
            graph1 = main_graph(export_df, "NYISpjm shock X forecast", "NYIS pjm DA regular prediction", "NYIS pjm DA", display, main_table_slider, True)
            table1 = main_table_state
        except Exception as e:
            pass
        
    if triggered_id == "main_table2_data":
        try:
            export_df = parse_table_data(main_table2_data_state, df.index)
            if not export_df.empty:
                export_df.set_index('Datetime (HB)', inplace=True)
                export_df["PJM nyis DA"] = df["PJM nyis DA"]
            graph2 =  main_graph(export_df, "PJMnyis shock X forecast", "PJM nyis DA regular prediction", "PJM nyis DA", display, main_table2_slider, True)
            table2 = main_table2_state
        except:
            pass
    # Return the updated figures and table components
    return graph1, graph2, graphS, graphS2, table1, table2, slider_className, slider_className


# Run the Dash application
if __name__ == "__main__":
    app.run_server(debug=True)
