import pandas as pd
from backend.data_setup import calculate_user_predictions

def assign_color(df, col1, col2, base_zero=False):
    """
    This function assigns colors based on the comparison between two columns in a DataFrame.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data to be evaluated.
    col1 (str): The name of the first column to compare.
    col2 (str): The name of the second column to compare.
    base_zero (bool, optional): A boolean flag indicating whether the comparison should be 
                                against 0 instead of `col2`. Defaults to False.
    
    Returns:
    list: A list of RGBA color strings ('rgba(r, g, b, a)') assigned to each row based 
          on the comparison results.
    """
    # Initialize an empty list to store the color values
    colors = []
    
    # Iterate through each row of the DataFrame
    for i, row in df.iterrows():
        
        # Check if the value in col1 is greater than col2 (or 0 if base_zero is True)
        if row[col1] > (0 if base_zero else row[col2]):
            # Append a green color with some transparency if the condition is met
            colors.append('rgba(0, 255, 0, 0.7)')
        
        # Check if the value in col2 (or 0 if base_zero is True) is greater than col1
        elif (0 if base_zero else row[col2]) > row[col1]:
            # Append a red color with some transparency if the condition is met
            colors.append('rgba(255, 0, 0, 0.7)')
        
        # If neither condition is met, append a transparent color
        else:
            colors.append('rgba(0, 0, 0, 0)')
    
    # Return the list of assigned colors
    return colors


def parse_table_data(data, df_index):
    df = pd.DataFrame(data)
    df = df.set_index("Hour").T
    if not df.empty:
        df.insert(0, 'Datetime (HB)', df_index)
    return df


    