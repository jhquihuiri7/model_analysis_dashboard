from backend.Class import Ops
from datetime import date, time, datetime, timedelta

def calculate_user_predictions(df, lower_prediction_column_str, upper_prediction_column_str, slider_percentage):
    percentage = slider_percentage / 100.0
    user_predictions = []
    for index, row in df.iterrows():
        regular_model = row[lower_prediction_column_str]
        shock_model = row[upper_prediction_column_str]
        abs_difference = abs(shock_model - regular_model)
        if shock_model > regular_model:
            prediction = regular_model + (abs_difference * percentage)
        else:
            prediction = shock_model + (abs_difference * percentage)
        user_predictions.append(prediction)
    return user_predictions

def setup_data():

    start_date = "2024-12-15"
    end_date = "2024-12-31"
    features_list = [
        "PJM nyis DA",
        "NYIS pjm DA",
        "PJMnyis shock X forecast",
        "NYISpjm shock X forecast",
        "PJM nyis DA regular prediction",
        "NYIS pjm DA regular prediction",
    ]
    
    actual = Ops()
    actual.update_data_features(features_list)
    actual.update_date_range(start_date, end_date)
    actual.update_df()
    actual.create_feature(
        [
            {"Feature": "NYISpjm shock X forecast"},
            {"Feature": "PJMnyis shock X forecast", "Operation": "-"},
        ],
        False,
        "PJM to NYIS shock predicted spread",
    )
    
    actual.create_feature(
        [
            {"Feature": "NYIS pjm DA regular prediction"},
            {"Feature": "PJM nyis DA regular prediction", "Operation": "-"},
        ],
        False,
        "PJM to NYIS regular predicted spread",
    )
    
    actual.update_data_features(features_list)

    actual.create_feature([{"Feature": "PJM nyis DA"},{"Feature": "NYIS pjm DA", "Operation": "-"}], False, "NYIS to PJM spread")
    actual.create_feature([{"Feature": "PJMnyis shock X forecast"},{"Feature": "NYISpjm shock X forecast", "Operation": "-"}], False, "NYIS to PJM shock spread")
    actual.create_feature([{"Feature": "NYIS pjm DA"},{"Feature": "PJM nyis DA", "Operation": "-"}], False, "PJM to NYIS spread")
    actual.create_feature([{"Feature": "NYISpjm shock X forecast"},{"Feature": "PJMnyis shock X forecast", "Operation": "-"}], False, "PJM to NYIS shock spread")
    
    return actual


# Predict toggle: 
#   ✓ When this toggle is off it should show the layout described below with all the data in the dataframe
#   but the tables should be hidden. 
#   ✓ When the toggle is on it should only show the last day of data in the dataframe with the exact layout described below.

# App layout:
#   Graph one should show the regular forcast(NYIS pjm DA regular prediction), the shock forcast(NYISpjm shock X forecast), and the actuals(NYIS pjm DA) for NYIS pjm.
#       When the shock forcast is greater than the regualr forcast highlight the area bettweent the two forcasts in green,
#       when the regualr forcast is greater than the shock forcast highlight the area in red.
#       Then the table assosiated with this graph should be right underneath this graph.
#       Row one of the table should be the hours (0-23), row two is the shock forcast, and row three is the regular forcast

#   Graph two should be the same as Graph one but for PJM nyis (including the assosiated table)

#   Graph three should be the shock model predicted spread and graph four should be the regular model predicted spread
#       When the spread is greater than 0 highlight the area between the x-axis and the line in green, when less than 0 highlight in red
