import os
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import numpy as np
import math

ALLOWED_TYPES = (
    "number",
)

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

layout = {'title': {'text':'3D'}}

fig = go.Figure(data=[go.Surface(x = X, y = Y, z = Z)], layout=layout)

# ---------- Display ----------

app = dash.Dash()
app.title = "Steepest Descent"

server = app.server

badge = dbc.Button(
    [
        "Start",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)
app.layout = html.Div([
    #graph
    html.Div(
        children=[dcc.Graph(id='my-graph', figure=fig)]
    ),
    #slider
    dcc.Slider(
        id='my-slider',
        min=0,
        max=7,
        step=1,
        value=0,
    ),

    html.Div(id='slider-output-container'),

    ]
    #button




)



# @app.callback(
#     dash.dependencies.Output('container-button-timestamp', 'children'),
#     [dash.dependencies.Input('btn-nclicks-1', 'n_clicks'),
#     dash.dependencies.Input('btn-nclicks-2', 'n_clicks'),
#     dash.dependencies.Input('btn-nclicks-3', 'n_clicks')]
# )
# def displayClick(btn1, btn2, btn3):
#     changed_id = [p['prop_id'] for p in callback_context.triggered][0]
#     if 'btn-nclicks-1' in changed_id:
#         msg = 'Button 1 was most recently clicked'
#     elif 'btn-nclicks-2' in changed_id:
#         msg = 'Button 2 was most recently clicked'
#     elif 'btn-nclicks-3' in changed_id:
#         msg = 'Button 3 was most recently clicked'
#     else:
#         msg = 'None of the buttons have been clicked yet'
#     return html.Div(msg)


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    dash.dependencies.Input('my-slider', 'value')

)
def update_output(value):
    return 'You have selected t="{}"'.format(value)
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)