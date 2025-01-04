import dash_mantine_components as dmc
import numpy as np

# Dash imports
from dash import html

def main_table(df, cols, id, display=False):
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
    
    # Filter the DataFrame to show data for the most recent day
    if not df.empty:  
        last_day = df.index.max().date()  # Get the latest date from the DataFrame index
        df = df[df.index.date == last_day]  # Filter rows for the latest day

    # Create table rows for each column in the specified `cols` list
    rows = [
        dmc.TableTr(  # Create a table row
            [dmc.TableTd(col)] +  # The first cell in each row contains the column name
            [
                # Add the values from the DataFrame, rounded to 2 decimal places
                dmc.TableTd(round(value, 2)) for value in (np.zeros(24) if df.empty else df[col])
            ]
        )
        for col in cols  # Iterate over the list of columns to generate the rows
    ]
    
    # Create the table header with a row containing the "Model" label and hours 0-23
    head = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Model"),  # First header cell for the "Model" column
                *[dmc.TableTh(hour) for hour in range(0, 24)]  # Header cells for each hour from 0 to 23
            ]
        )
    )
    
    # Create the table body using the generated rows
    body = dmc.TableTbody(rows)
    
    # Return a Div element containing the table with specific styles
    return html.Div(
        dmc.Table(
            [head, body],  # Add the header and body to the table
            withTableBorder=True,  # Add a border around the table
            highlightOnHover=True,  # Highlight rows when hovered
            className="rounded-lg border border-separate border-tools-table-outline mb-12",  # Table styling
            style={'display': 'inline'} if display else {'display': 'none'},  # Display table based on `display` flag
        ),
        id=id  # Assign the specified ID to the Div element
    )
