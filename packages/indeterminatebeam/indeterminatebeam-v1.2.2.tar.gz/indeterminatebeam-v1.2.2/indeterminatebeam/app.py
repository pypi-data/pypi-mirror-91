# https://medium.com/analytics-vidhya/python-dash-data-visualization-dashboard-template-6a5bff3c2b76 
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from indeterminatebeam import Beam, Support, PointLoad,PointTorque,DistributedLoadV,TrapezoidalLoad
import dash_table

import time

import plotly.express as px

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

##the controls for the sidebar
controls = dbc.FormGroup()

sidebar = html.Div(
    [
        html.H2('About', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)



##Properties for Beam Tab

beam_table_data = {
    'Length':5, 
    "Young's Modulus (MPa)":2*10**5,
    "Second Moment of Area (mm4)":9.05*10**6, 
    "Cross-Sectional Area (mm2)":2300
    }

beam_table = dash_table.DataTable(
        id='beam-table',
        columns=[{
            'name': i,
            'id': i,
            'deletable': False,
            'renamable': False
        } for i in beam_table_data.keys()],
        data=[beam_table_data],
        editable=True,
        row_deletable=False
    )

beam_content = dbc.Card(
    dbc.CardBody(
        [
            beam_table,
        ]
    ),
    className="mt-3",
)

##Properties for Support Tab
support_table_data = {
    'x_coordinate':0, 
    "Young's Modulus, E (MPa)":2*10**5,
    "Second Moment of Area, I (mm4)":9.05*10**6, 
    "Cross-Sectional Area, A (mm2)":2300
    }

support_table = dash_table.DataTable(
        id='support-table',
        columns=[{
            'name': i,
            'id': i,
            'deletable': False,
            'renamable': False
        } for i in support_table_data.keys()],
        data=[support_table_data],
        editable=True,
        row_deletable=True
    )

support_content = dbc.Card(
    dbc.CardBody(
        [
            support_table,
            html.Br(),
            html.Button('Add Support', id='support-rows-button', n_clicks=0),
        ]
    ),
    className="mt-3",
)

##Properties for point_load Tab
point_load_table_data = {
    "x_coordinate (m)":1,
    "Force (kN)":0, 
    "Angle (deg)":90, 
    }

point_load_table = dash_table.DataTable(
        id='point-load-table',
        columns=[{
            'name': i,
            'id': i,
            'deletable': False,
            'renamable': False
        } for i in point_load_table_data.keys()],
        data=[point_load_table_data],
        editable=True,
        row_deletable=True
    )

point_load_content = dbc.Card(
    dbc.CardBody(
        [
            point_load_table,
            html.Br(),
            html.Button('Add Point Load', id='point-load-rows-button', n_clicks=0),
        ]
    ),
    className="mt-3",
)

##Properties for point_torque Tab
point_torque_table_data = {
    "x_coordinate (m)":1,
    'Torque (kN.m)':0, 
    }

point_torque_table = dash_table.DataTable(
        id='point-torque-table',
        columns=[{
            'name': i,
            'id': i,
            'deletable': False,
            'renamable': False
        } for i in point_torque_table_data.keys()],
        data=[point_torque_table_data],
        editable=True,
        row_deletable=True
    )

point_torque_content = dbc.Card(
    dbc.CardBody(
        [
            point_torque_table,
            html.Br(),
            html.Button('Add Point Torque', id='point-torque-rows-button', n_clicks=0),
        ]
    ),
    className="mt-3",
)

##Properties for distributed_load Tab
distributed_load_table_data = {
    'Start x_coordinate (m)':0,
    'End x_coordinate (m)': 0,
    'Start Load (kN/m)':0,
    'End Load (kN/m)':0,
    }

distributed_load_table = dash_table.DataTable(
        id='distributed-load-table',
        columns=[{
            'name': i,
            'id': i,
            'deletable': False,
            'renamable': False
        } for i in distributed_load_table_data.keys()],
        data=[distributed_load_table_data],
        editable=True,
        row_deletable=True
    )

distributed_load_content = dbc.Card(
    dbc.CardBody(
        [
            distributed_load_table,
            html.Br(),
            html.Button('Add Distributed Load', id='distributed-load-rows-button', n_clicks=0),
            
        ]
    ),
    className="mt-3",
)

##Properties for query tab
query_table_data = {
    'query coordinate (m)':0,
    }

query_table = dash_table.DataTable(
        id='query-table',
        columns=[{
            'name': i,
            'id': i,
            'deletable': False,
            'renamable': False
        } for i in query_table_data.keys()],
        data =[],
        editable=True,
        row_deletable=True
    )

query_content = dbc.Card(
    dbc.CardBody(
        [
            query_table,
            html.Br(),
            html.Button('Add Query', id='query-rows-button', n_clicks=0),
            
        ]
    ),
    className="mt-3",
)
##assemble different input tabs

tabs = dbc.Tabs(
    [
        dbc.Tab(beam_content, label="Beam"),
        dbc.Tab(support_content, label="Supports"),
        dbc.Tab(point_load_content, label="Point Loads"),
        dbc.Tab(point_torque_content, label="Point Torques"),
        dbc.Tab(distributed_load_content, label="Distributed Load"),
        dbc.Tab(query_content, label="Query")
    ]
)

##create a submit button
submit_button = dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        )

content_first_row = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Card(
                    dbc.Spinner(dcc.Graph(id='graph_1')),           
                    ),
                html.Br(),
                tabs,
                html.Br(),
                submit_button

            ],
            md = 6
        ),

        dbc.Col(
            dbc.Card(
                dbc.Spinner(dcc.Graph(id='graph_2'))
                ), 
            md = 6
        )

    ]
)


content = html.Div(
    [
        html.H2('Beam Calculator Proof of Concept', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
    ],
    style=CONTENT_STYLE
)


app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
app.layout = html.Div([sidebar,content])

##calculation for internal forces, plot
@app.callback(
    [Output('graph_1', 'figure'),Output('graph_2', 'figure')],
    [Input('submit_button', 'n_clicks')],
    [State('beam-table', 'data'), State('point-load-table','data'),
    State('point-torque-table','data'),State('query-table','data'),
    State('distributed-load-table','data')]
    )
def analyse_beam(click, beams,point_loads,point_torques,querys,distributed_loads):

    for row in beams:
        beam = Beam(*(float(a) for a in row.values()))

    a = Support(0,(1,1,1))

    beam.add_supports(a)

    if point_loads:
        for row in point_loads:
            print(row)
            beam.add_loads(PointLoad(
                float(row['Force (kN)']),
                float(row['x_coordinate (m)']),
                float(row['Angle (deg)'])
                )
            )
            
    if point_torques:
        for row in point_torques:
            beam.add_loads(PointTorque(
                float(row['Torque (kN.m)']),
                float(row['x_coordinate (m)']),
                )
            )

    if distributed_loads:
        for row in distributed_loads:
            if abs(float(row['Start x_coordinate (m)'])) > 0 or \
               abs(float(row['End x_coordinate (m)'])) > 0:
                beam.add_loads(TrapezoidalLoad(
                    force = (
                        float(row['Start Load (kN/m)']),
                        float(row['End Load (kN/m)'])
                    ),
                    span = (
                        float(row['Start x_coordinate (m)']),
                        float(row['End x_coordinate (m)'])
                    ))
                )
    beam.analyse()

    if querys:
        for row in querys:
            beam.add_query_points(
                float(row['query coordinate (m)']),
                )

    graph_1 = beam.plot_beam_external()
    graph_2 = beam.plot_beam_internal()

    return graph_1, graph_2


@app.callback(
    Output('support-table', 'data'),
    Input('support-rows-button', 'n_clicks'),
    State('support-table', 'data'),
    State('support-table', 'columns'))
def add_row2(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append(support_table_data)
    return rows

@app.callback(
    Output('point-load-table', 'data'),
    Input('point-load-rows-button', 'n_clicks'),
    State('point-load-table', 'data'),
    State('point-load-table', 'columns'))
def add_row3(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append(point_load_table_data)
    return rows

@app.callback(
    Output('point-torque-table', 'data'),
    Input('point-torque-rows-button', 'n_clicks'),
    State('point-torque-table', 'data'),
    State('point-torque-table', 'columns'))
def add_row4(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append(point_torque_table_data)
    return rows

@app.callback(
    Output('distributed-load-table', 'data'),
    Input('distributed-load-rows-button', 'n_clicks'),
    State('distributed-load-table', 'data'),
    State('distributed-load-table', 'columns'))
def add_row5(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append(distributed_load_table_data)
    return rows

@app.callback(
    Output('query-table', 'data'),
    Input('query-rows-button', 'n_clicks'),
    State('query-table', 'data'),
    State('query-table', 'columns'))
def add_row6(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append(query_table_data)
    return rows

if __name__ == '__main__':
    app.run_server(port='8085')