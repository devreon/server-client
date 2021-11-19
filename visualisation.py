import os
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

import numpy as np
import math

# ---------- Initialize X, Y, Z ----------

def f(x, y):
    return 1/2 * (math.pow(x+y,4)+math.pow(x-y,4))

X = np.arange(-10, 11, 1)
Y = X
Z = np.zeros((21,21))

for i in range(21):
    for j in range(21):
        Z[i][j] = f(X[i], Y[j])

# ---------- Generate graphs ----------

layout = {'title': {'text':'DISPLAY ME!'}}

fig = go.Figure(data=[go.Surface(x = X, y = Y, z = Z)], layout=layout)

# ---------- Display ----------

app = dash.Dash()
app.title = "Steepest Descent"

server = app.server

app.layout = html.Div([
    html.Div(
        children=[dcc.Graph(id='my-graph', figure=fig)]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)