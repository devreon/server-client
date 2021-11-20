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
    return 1/2 * (math.pow(x+y, 4)+math.pow(x-y, 4))      # math.sin(x*x+y*y)/((x*x+y*y))

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
        children=[dcc.Graph(id='my-graph', figure=fig, style={'width': '50vh', 'height': '50vh', 'display':'inline-block'})]
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


    # button
    # x
    html.Div(dcc.Input(id='inputX_start', type='number', placeholder="x_start=")),
    html.Div(dcc.Input(id='inputX_change', type='number', placeholder="x_change=")),
    html.Div(dcc.Input(id='inputX_end', type='number', placeholder="x_end=")),

    # y
    html.Div(dcc.Input(id='inputY_start', type='number', placeholder="y_start=")),
    html.Div(dcc.Input(id='inputY_change', type='number', placeholder="y_change=")),
    html.Div(dcc.Input(id='inputY_end', type='number', placeholder="y_end=")),

    # t

    html.Div(dcc.Input(id='inputT_start', type='number', placeholder="t_start=")),
    html.Div(dcc.Input(id='inputT_change', type='number', placeholder="t_change=")),
    html.Div(dcc.Input(id='inputT_end', type='number', placeholder="t_end=")),


    html.Div(id='container', children=''),

    html.Button('Submit', id='submit', n_clicks=0),

]
)





@app.callback(
    dash.dependencies.Output('container', 'children'),
    dash.dependencies.Input('submit', 'n_clicks'),
    [dash.dependencies.State('inputX_start', 'value'),
     dash.dependencies.State('inputX_change', 'value'),
     dash.dependencies.State('inputX_end', 'value'),
     dash.dependencies.State('inputY_start', 'value'),
     dash.dependencies.State('inputY_change', 'value'),
     dash.dependencies.State('inputY_end', 'value'),
     dash.dependencies.State('inputT_start', 'value'),
     dash.dependencies.State('inputT_change', 'value'),
     dash.dependencies.State('inputT_end', 'value'),
     ],
)
def update_output(n_clicks, x_start, x_change, x_end, y_start, y_change, y_end, t_start, t_change, t_end):
    # так можно доставать вытащить значения для callback элемента.
    # X=value
    # print(X)
    return 'The input value was {}_____{}_____{}_____{}_____{}_____{}_____{}_____{}_____{}_____  '.format(
         x_start, x_change, x_end,y_start, y_change, y_end, t_start, t_change, t_end, n_clicks

    )


# slider callback for t .
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    dash.dependencies.Input('my-slider', 'value')

)
def update_output(value):
    # printedvalue=value
    # print(printedvalue)
    return 'You have selected t="{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)