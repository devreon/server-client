import os
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import numpy as np
import math

X = []
Y = []
Z = []
T = []

X_input = []
Y_input = []
T_input = []
Z_input = []


# ---------- Initialize X, Y, Z ----------
def f(x, y, t):
    return (1 / 2 * (math.pow(x + y, 4) + math.pow(x - y, 4)))*t  # math.sin(x*x+y*y)/((x*x+y*y))



def calculate(X,Y,Z,t):
    for i in np.arange(len(X)):
        for j in np.arange(len(Y)):
            Z[i][j] = f(X[i], Y[j],t)





# ---------- Generate graphs ----------
layout = {'title': {'text': '3D'}}

fig = go.Figure(data=[go.Mesh3d(x=X, y=Y, z=Z)], layout=layout)

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
        #children=[dcc.Graph(id='my-graph', figure=fig, style={'width': '50vh', 'height': '50vh', 'display':'inline-block'})]
        dcc.Graph(id='my-graph', figure=fig, style={'width': '50vh', 'height': '50vh', 'display':'inline-block'})
    ),
    # slider

    dcc.Slider(
        id='my-slider',
        min=0,
        max=0,
        step=0,
        value=0,

        marks={},
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
    if not n_clicks:
        return( x_start, x_change, x_end, y_start, y_change, y_end, t_start, t_change, t_end)

    print(x_start)
    print(x_change)
    print(x_end)
    for i in np.arange(x_start, x_end, x_change):
        X_input.append(i)
    for i in np.arange(y_start, y_end, y_change):
        Y_input.append(i)
    for i in np.arange(t_start, t_end, t_change):
        T_input.append(i)





    return 'The input value was {}_____{}_____{}_____{}_____{}_____{}_____{}_____{}_____{}_____  '.format(
         x_start, x_change, x_end,y_start, y_change, y_end, t_start, t_change, t_end, n_clicks

    )


@app.callback(
    dash.dependencies.Output("my-slider", "min"),
    dash.dependencies.Output("my-slider", "max"),
    dash.dependencies.Output("my-slider", "value"),
    dash.dependencies.Output("my-slider", "step"),
    dash.dependencies.Output("my-slider", "marks"),
    dash.dependencies.Input("submit", "n_clicks"),
    dash.dependencies.State("my-slider", "min"),
    dash.dependencies.State("my-slider", "max"),
    dash.dependencies.State("my-slider", "value"),
    dash.dependencies.State("my-slider", "step"),
    dash.dependencies.State("my-slider", "marks"),
    dash.dependencies.State('inputT_start', 'value'),
    dash.dependencies.State('inputT_change', 'value'),
    dash.dependencies.State('inputT_end', 'value'),
)
def update_slider(nClicks, sliderMin, sliderMax, sliderValue, sliderStep, sliderMarks,t_start, t_change, t_end):

    if not nClicks:
        return (sliderMin, sliderMax, sliderValue,sliderStep, sliderMarks)

    if isinstance(t_change, int):
        return (t_start, t_end, 0, t_change, {i: '{}'.format(i) for i in range(t_start, t_end + t_change, t_change)})
    else:
        return (t_start, t_end, 0, t_change, {i: '{}'.format(i) for i in np.arange(t_start, t_end + t_change, t_change)})



# slider callback for t .  graphic
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    dash.dependencies.Input('my-slider', 'value')
)
def update_output(value):
    # printedvalue=value
    # print(printedvalue)
    return 'You have selected t="{}"'.format(value)


@app.callback(dash.dependencies.Output('my-graph', 'figure'),
              [dash.dependencies.Input('my-slider', 'value')]
              )
def update_graph(value):
    tvalue = value

    Z_input = np.zeros((len(X_input), len(X_input)))

    X = X_input
    Y = Y_input
    Z = Z_input
    #check if mesh is correct
    pts = np.loadtxt(np.DataSource().open('https://raw.githubusercontent.com/plotly/datasets/master/mesh_dataset.txt'))
    x, y, z = pts.T
    x= x*value*value
    y=y*value
    z=z*value
    calculate(X, Y, Z, tvalue)
    # X=  X_input
    # Y = Y_input
    # Z = Z_input

    fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z)], layout=layout)
    return fig












if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)