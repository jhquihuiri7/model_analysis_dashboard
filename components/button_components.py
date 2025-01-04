import dash_daq as daq

# Import the HTML module from Dash
from dash import html

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
