import os
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import numpy as np
import math

t_min = 0
t_max = 10
t_change = 1
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
    # graph
    html.Div(  # size of plot in style
        children=[dcc.Graph(id='my-graph', figure=fig, style={'width': '70vh', 'height': '70vh', 'display':'inline-block'})]
    ),
    # slider
    dcc.Slider(
        id='my-slider',
        min=t_min,
        max=t_max,
        step=1,
        value=0,

        marks={i: '{}'.format(i) for i in range(t_max+t_change)},
    ),

    html.Div(id='slider-output-container'),


    #button
    html.Div(dcc.Input(id='inputX', type='text')),
    html.Button('Submit', id='submitX', n_clicks=0),
    html.Div(id='containerX', children='Enter a value and press submit'),

    html.Div(dcc.Input(id='inputY', type='text')),
    html.Button('Submit', id='submitY', n_clicks=0),
    html.Div(id='containerY', children='Enter a value and press submit')


]
)
@app.callback(
    dash.dependencies.Output('containerY', 'children'),
    dash.dependencies.Input('submitY', 'n_clicks'),
    dash.dependencies.State('inputY', 'value'),

)
def update_output(n_clicks, value):
    # так можно доставать вытащить значения для callback элемента.
    # X=value
    # print(X)
    return 'The input value was "{}"  '.format(
        value

    )
@app.callback(
    dash.dependencies.Output('containerX', 'children'),
    dash.dependencies.Input('submitX', 'n_clicks'),
    dash.dependencies.State('inputX', 'value'),

)
def update_output(n_clicks, value):
    # так можно доставать вытащить значения для callback элемента.
    # X=value
    # print(X)
    return 'The input value was "{}"  '.format(
        value

    )

# slider callback for t .
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    dash.dependencies.Input('my-slider', 'value')

)
def update_output(value):
    #printedvalue=value
    #print(printedvalue)
    return 'You have selected t="{}"'.format(value)





if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)