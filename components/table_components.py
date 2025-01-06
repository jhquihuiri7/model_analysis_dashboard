import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from backend.data_setup import calculate_user_predictions
# Dash imports
from dash import html, dcc
import dash_ag_grid as dag

def main_table(df, cols, id, display=False, slider_value=0 ):
    """
    This function generates a table using Dash components to display a DataFrame.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data to be displayed.
    cols (list): A list of column names to display in the table.
    id (str): The ID to be assigned to the main Div element containing the table.
    display (bool, optional): A flag that controls whether the table should be visible. 
                              Defaults to False (hidden).
    
    Returns:
    dash_html_components.Div: A Div element containing a Dash table with the data from `df`.
    """
    
    data = pd.DataFrame(0, index=range(3), columns=["Hour"])
    data["Hour"] = cols + ["User Prediction"]
    for i in range(0,24):
        data[i] = 0

    # Filter the DataFrame to show data for the most recent day
    if not df.empty:  
        last_day = df.index.max().date()  # Get the latest date from the DataFrame index
        df = df[df.index.date == last_day]# Filter rows for the latest day
        for index, col in enumerate(cols):
            data.loc[index, "Hour"] = col
            data.iloc[index, 1:] = df[col]  # Aseguramos que el tamaño sea el adecuado
        data.loc[2, "Hour"] = "User Prediction"
        data.iloc[2, 1:] = calculate_user_predictions(df, cols[1], cols[0],slider_value)
  
    return html.Div(
        children = [
            dag.AgGrid(
            columnDefs=[
                {"field": str(col), "width": 150, 'suppressSizeToFit': True} if index == 0 else {"field": str(col)}
                for index, col in enumerate(data.columns)
            ],
            rowData=data.to_dict("records"),
            columnSize="sizeToFit",
            defaultColDef={"editable": True, "minWidth": 30},
            dashGridOptions={"animateRows": False, "rowSelection":'single'},
            style={"height": "100%", 'display': 'inline'} if display else {"height": "100%", 'display': 'none'},  # Display table based on `display` flag
        )
        ],
        className="w-full h-[180px] mb-10",
        id=id,
    )


