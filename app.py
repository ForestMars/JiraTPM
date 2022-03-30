#!/usr/bin/env python
# bar_chart.py - display stats for tickets created per minute over 1 hour period
__version__ = '0.0.1'
__author__ = 'Forest Mars'

import dash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

from data_loader import Handlers
from config.postgres import session_engine


css = ['assets/css/bar.css']
app = dash.Dash(__name__, external_stylesheets=css)
engine = session_engine()
handle = Handlers()
df = handle.load_pg()
#summary = df['seconds'].value_counts().sort_index().to_frame()
summary = df['seconds'].value_counts().sort_index()

x_data = df.index.values.tolist()
y_data = summary.tolist()
ticks = list(range(60))

fig = go.Figure(go.Bar(
    x = ticks,
    y = y_data,
))

fig.update_layout(
    yaxis = dict(
        tickmode = 'linear',
        tick0 = 1.0,
        dtick = 1.0,
    ),

)

app.layout = html.Div([
    html.H1('JIRA Tickets Per Minute'),
    html.H4('Showiing High or Highest severtity tickets over 1 hour period'),
    dcc.Graph(figure=fig),

])


if __name__ == '__main__':
    app.run_server(debug=True)
