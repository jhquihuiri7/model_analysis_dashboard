import plotly.graph_objects as go
from utils.logic_functions import assign_color

def main_graph(df, col1, col2, col3):
    """
    This function creates a Plotly graph comparing three different time series data 
    from the DataFrame, with color filling between two series based on their relative values.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the time series data.
    col1 (str): The name of the first column to be plotted.
    col2 (str): The name of the second column to be plotted.
    col3 (str): The name of the third column to be plotted.
    
    Returns:
    plotly.graph_objects.Figure: The Plotly figure object containing the graph.
    """
    
    # Initialize a new figure for the graph
    fig = go.Figure()
    
    # Add the first time series to the figure (NYISpjm shock x forecast)
    fig.add_trace(go.Scatter(x=df.index, y=df[col1], mode='lines', name="NYISpjm shock x forecast", line_shape='hv'))
    
    # Add the second time series to the figure (NYIS pjm DA regular prediction)
    fig.add_trace(go.Scatter(x=df.index, y=df[col2], mode='lines', name="NYIS pjm DA regular prediction", line_shape='hv'))
    
    # Add the third time series to the figure (Actuals)
    fig.add_trace(go.Scatter(x=df.index, y=df[col3], mode='lines', name="Actuals", line_shape='hv'))
    
    # Use the assign_color function to determine the color for each time period
    colors = assign_color(df=df, col1="NYISpjm shock X forecast", col2="NYIS pjm DA regular prediction")

    # Create shaded areas between the two time series (col2 and col1) based on their relative values
    for i in range(len(df)-1):
        fig.add_trace(go.Scatter(
            x=[df.index[i], df.index[i], df.index[i+1], df.index[i+1]],  # X coordinates for the shaded area
            y=[df[col2].iloc[i], df[col1].iloc[i], 
               df[col1].iloc[i], df[col2].iloc[i]],  # Y coordinates for the shaded area
            fill='toself', fillcolor=colors[i],  # Fill the area with the color determined earlier
            line=dict(color='rgba(255,255,255,0)'),  # Set the line to be transparent
            showlegend=False, hoverinfo='none'  # Hide the legend and hover information
        ))
    
    # Update the layout with axis labels, range, and legend settings
    fig.update_layout(
        #title='How Shocky will NYIS be?',  # Optionally, you can add a title
        xaxis_title='Datetime',  # Label for the X axis
        yaxis_title='Price',  # Label for the Y axis
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),  # Legend placement
        xaxis_range=[df.index.min(), df.index.max()],  # Set the X axis range to match the data
        margin=dict(t=0),  # Remove top margin
    )
    
    # Return the figure object
    return fig

def spread_graph(df, col1):
    """
    This function creates a Plotly graph for a single time series data 
    showing the predicted spread between PJM and NYIS Shock models.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the time series data.
    col1 (str): The name of the column to be plotted.
    
    Returns:
    plotly.graph_objects.Figure: The Plotly figure object containing the graph.
    """
    
    # Initialize a new figure for the spread graph
    fig = go.Figure()
    
    # Add the time series to the figure (PJM to NYIS Shock models predicted spread)
    fig.add_trace(go.Scatter(x=df.index, y=df[col1], mode='lines', 
                              name="PJM to NYIS Shock models predicted spread", line_shape='hv'))

    # Use the assign_color function to determine the color for the time periods
    colors = assign_color(df=df, col1=col1, col2=None, base_zero=True)

    # Create shaded areas beneath the time series to represent the spread
    for i in range(len(df) - 1):
        fig.add_trace(go.Scatter(
            x=[df.index[i], df.index[i], df.index[i+1], df.index[i+1]],  # X coordinates for the shaded area
            y=[0, df[col1].iloc[i], 
               df[col1].iloc[i], 0],  # Y coordinates for the shaded area
            fill='toself', fillcolor=colors[i],  # Fill the area with the color determined earlier
            line=dict(color='rgba(255,255,255,0)'),  # Set the line to be transparent
            showlegend=False, hoverinfo='none'  # Hide the legend and hover information
        ))

    # Update the layout with axis labels, range, and legend settings
    fig.update_layout(
        #title='PJM to NYIS Shock models predicted spread',  # Optionally, you can add a title
        xaxis_title='Datetime',  # Label for the X axis
        yaxis_title='Spread',  # Label for the Y axis
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),  # Legend placement
        xaxis_range=[df.index.min(), df.index.max()],  # Set the X axis range to match the data
        margin=dict(t=0),  # Remove top margin
    )
    
    # Return the figure object
    return fig