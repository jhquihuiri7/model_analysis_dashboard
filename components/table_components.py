import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from backend.data_setup import calculate_user_predictions
import utils.export_variables as variables
# Dash imports
from dash import html
import dash_ag_grid as dag

import warnings
warnings.filterwarnings("ignore")
#import app

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
        df["User Prediction"] = calculate_user_predictions(df, cols[1], cols[0],slider_value)
        for index, col in enumerate(cols+["User Prediction"]):
            data.loc[index, "Hour"] = col
            data.iloc[index, 1:] = df[col]
        data = data.round(2)
        if id == "main_table":
            variables.export_df1 = df[cols+["User Prediction"]]
        else:
            variables.export_df2 = df[cols+["User Prediction"]]
        
  
    return html.Div(
    children=[
        dag.AgGrid(
            columnDefs=[
                {"field": str(col), "width": 150, 'suppressSizeToFit': True} if index == 0 else {"field": str(col)}
                for index, col in enumerate(data.columns)
            ],
            rowData=data.to_dict("records"),
            columnSize="sizeToFit",
            defaultColDef={"editable": True, "minWidth": 30},
            dashGridOptions={"animateRows": False, "rowSelection": "single", "domLayout": "autoHeight"},
            style = {"height": None}
        )
    ],
    className="w-full mb-10 inline" if display else "w-full mb-10 hidden",
)


