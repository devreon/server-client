import os
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import numpy as np
import math
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

# ---------- Initialize X, Y, Z ----------


# ---------- Generate graphs ----------
layout = {'title': {'text': '3D'}}

fig = go.Figure(data=[go.Surface()], layout=layout)

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

    sa = gspread.service_account(filename='reciever/service_account.json')
    sh = sa.open("data")
    wks = sh.worksheet("list1")
    cell_list = wks.range('A2:I2')
    cell_values = [x_start, x_change, x_end, y_start, y_change, y_end, t_start, t_change, t_end]

    for i, val in enumerate(cell_values):  # gives us a tuple of an index and value
        cell_list[i].value = val  # use the index on cell_list and the val from cell_values

    wks.update_cells(cell_list)


    #fig.update_xaxes(range=[x_start, x_end])
    #fig.update_yaxes(range=[y_start, y_end])


    return 'The input value was {}_____{}_____{}_____{}_____{}_____{}_____{}_____{}_____{}_____  '.format(
         round(x_start,5), round(x_change,5), round(x_end,5),round(y_start,5), round(y_change,5), round(y_end,5), round(t_start,5), round(t_change,5), round(t_end, 5), n_clicks


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

    tvalue = value #V CALCULATE



    Z_transpose =Z.transpose()



    fig = go.Figure(data=[go.Surface(x=X, y=Y, z= Z_transpose)], layout=layout)




    # if (len(X) != 0 and len(Y) != 0 and len(Z) != 0):
    #     asp_x = X[-1]
    #     asp_y = Y[-1]
    #     asp_z = abs(max(max(x) for x in Z_transpose))
    #     #print('Z_transpose',Z_transpose[-1])
    # if (len(X) != 0 and len(Y) != 0 and len(Z) != 0):
    #     fig.update_layout(
    #     scene=dict(
    #         xaxis=dict(nticks=4, range=[X[0], X[-1]], ),
    #         yaxis=dict(nticks=4, range=[Y[0], Y[-1]], ),
    #         zaxis=dict(nticks=4, range=([Z_transpose[0], Z_transpose[-1]]), ),
    #         #aspectmode='manual',  #try to find good aspectmode to fix xyz size
    #
    #
    #         aspectratio=dict(x=asp_x, y=asp_y, z=asp_x),
    #     ),
    #     width=700,
    #
    #
    #     )
    #     name = 'default'
    #     camera = dict(
    #      eye=dict(x=asp_x, y=asp_y, z=asp_x)
    #     )
    #
    #     fig.update_layout(scene_camera= camera, title=name)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)