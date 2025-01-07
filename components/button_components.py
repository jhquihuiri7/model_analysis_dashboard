import dash_daq as daq

# Import the HTML module from Dash
from dash import html, dcc

from styles.styles import button_style

def button(text, id, style):
    """
    Creates an HTML button with custom properties.

    Args:
        text (str): The text to display on the button.
        id (str): A unique identifier for the button.
        style (str): A CSS class name to apply styles to the button.

    Returns:
        dash.html.Button: A button component with the specified properties.
    """
    # Create and return an HTML button with the given parameters
    return html.Button(
        text,        # Text displayed on the button
        id=id,       # Unique ID for the button
        n_clicks=0,  # Initial click count set to 0
        className=style  # CSS class for styling the button
    )

def last_day_toggle():
    """
    This function generates a Dash ToggleSwitch component inside a Div element, 
    allowing the user to toggle between showing the last 24 hours of data.
    
    Returns:
    dash_html_components.Div: A Div containing a ToggleSwitch for selecting 
                              the last 24-hour data.
    """
    
    # Return a Div containing the ToggleSwitch component with specific attributes
    return html.Div(
        daq.ToggleSwitch(
            id='last_day_toggle',  # Unique ID for the toggle switch
            value=False,  # Default value (False means the switch is off, or not showing the last 24 hours)
            label='Show last 24 hour data',  # The label displayed next to the toggle switch
            labelPosition='right',  # Position the label to the right of the switch
            color="#1975fa",  # Color of the toggle switch (blue)
            disabled=False  # The toggle switch is enabled by default
        ),
        className="ml-5 w-[150px] mb-5"  # CSS class for layout: margin-left, width, and bottom margin
    )

def table_slider(id, download_id, display=False):
    return html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H3("Adjust predictions offset ", className="mb-2"),
                            button(text="↓", id=download_id, style=button_style),       
                        ],
                        className="flex flex-row justify-between"
                    ),
                    dcc.Slider(min=0, max=100, step=10, value=0, 
                           marks={i: f"{i}%" for i in range(0, 101, 10)},
                           id=id
                    )
                ],
                id=f"{id}_container",
                className="inline mt-5 w-full" if display else "hidden mt-5 w-full"
            )