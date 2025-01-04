import plotly.graph_objects as go
import numpy as np
from utils.logic_functions import assign_color

def main_graph(client, col1, col2, col3):

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=client.df.index, y=client.df[col1], mode='lines', name="NYISpjm shock x forecast", line_shape='hv'))
    fig.add_trace(go.Scatter(x=client.df.index, y=client.df[col2], mode='lines', name="NYIS pjm DA regular prediction", line_shape='hv'))
    fig.add_trace(go.Scatter(x=client.df.index, y=client.df[col3], mode='lines', name="Actuals", line_shape='hv'))
    
    colors = assign_color(client=client, col1="NYISpjm shock X forecast", col2="NYIS pjm DA regular prediction")

    for i in range(len(client.df)-1):
        fig.add_trace(go.Scatter(
            x=[client.df.index[i], client.df.index[i], client.df.index[i+1], client.df.index[i+1]],
            y=[client.df[col2].iloc[i], client.df[col1].iloc[i], 
               client.df[col1].iloc[i], client.df[col2].iloc[i]],
            fill='toself', fillcolor=colors[i], line=dict(color='rgba(255,255,255,0)'),
            showlegend=False, hoverinfo='none'
        ))
    
    fig.update_layout(
        #title='How Shocky will NYIS be?',
        xaxis_title='Datetime',
        yaxis_title='Price',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis_range=[client.df.index.min(), client.df.index.max()]
    )
    
    return fig

def spread_graph(client):
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=client.df.index, y=client.df["PJM to NYIS shock spread"], mode='lines', 
                              name="PJM to NYIS Shock models predicted spread", line_shape='hv'))

    colors = assign_color(client=client, col1="PJM to NYIS shock spread", col2=None, base_zero=True)

    for i in range(len(client.df) - 1):
        fig.add_trace(go.Scatter(
            x=[client.df.index[i], client.df.index[i], client.df.index[i+1], client.df.index[i+1]],
            y=[0, client.df["PJM to NYIS shock spread"].iloc[i], 
               client.df["PJM to NYIS shock spread"].iloc[i], 0],
            fill='toself', fillcolor=colors[i], line=dict(color='rgba(255,255,255,0)'),
            showlegend=False, hoverinfo='none'
        ))

    fig.update_layout(
        #title='PJM to NYIS Shock models predicted spread',
        xaxis_title='Datetime',
        yaxis_title='Spread',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis_range=[client.df.index.min(), client.df.index.max()]
    )
    return fig
    
    