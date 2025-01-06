import Class
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

actual = Class.Ops()
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

# Prediction table description:
# The first row should be the hours, row two should be regular model predictions and row three should be the shock model predictions
# Row four is for user predictions. 
# the user will use a slider that is right below the table to make there predictions.
# For branch one the user should select which model of the two in the table they would like to offset from and then use
# the slider to offset from that model. there should be another branch where we use a slider to do a percentage from the 
# regular model to the shock model. 
# There is a function at the top of this file which has the logic to generate the user pedictions given a percentage, 
# the df, the regular prediction column name and the shock prediction column name.
# The user sould also be able to manualy change they're selections after the predictions are made using the slider

# Predict toggle: when this toggle is off it should show the layout described underneath with all the data in the dataframe
# but the tables should be hidden and the user predictions should not be displayed on the graphs. 
# When the toggle is on it should only show the last day of data in the dataframe with the exact layout described below

# App layout:
# Graph one should show the regular forcast, the shock forcast, the actuals, and the user predictions for NYIS pjm.
# When the shock forcast is greater than the regualr forcast highlight the area bettweent the two lines in green,
# when the regualr forcast is greater than the shock forcast highlight the area in red.
# Then the table and slider assosiated with this graph should be right underneath this graph.
# columns for graph one:  "NYIS pjm DA", "NYISpjm shock X forecast", "NYIS pjm DA regular prediction" and when
# the prediction toggle is on we should show the user predictions on the graph as they are adjusting the slider and 
# making manual changes

# Graph two should be the same as Graph one but for PJM nyis (including the assosiated table)
# Graph two columns: "PJM nyis DA", "PJMnyis shock X forecast", "PJM nyis DA regular prediction" and user predictions when toggle is on

# Graph three should be the shock model predicted spread and graph four should be the regular model predicted spread
# when the spread is greater than 0 highligh the area between teh x-axis and the line in green, when less than 0 highlight in red