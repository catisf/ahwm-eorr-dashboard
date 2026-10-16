
################################
######## ATTAINMENT PAGE #######
################################

# %% import dependencies
import plotly.express as px
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from load_data import get_att_data

# %% get data
df_att_combined, LAs = get_att_data()

# get plotting functions
from attainment_plots import PLOT_FUNCTIONS

# %% 
# page layout

dash.register_page(__name__)

la_dropdown = html.Div([
    html.P('Local Authority:'),
    dcc.Dropdown(LAs, 'National', id='la-dropdown')]
                            )

student_dropdown = html.Div([
    html.P('Student characteristic:'),
    dcc.Dropdown(df_att_combined['breakdown_topic'].unique(),
                 'FSM status',
                 id='student-dropdown')]
                        )
measure = html.Div([
    html.P('Measure:'),
    dcc.RadioItems(['Attainment 8',
                    '4 or above in English and maths GCSEs',
                    '5 or above in English and maths GCSEs'],
                    'Attainment 8',
                    id='att-measure',
                    inline=True)]
                            )

years = df_att_combined['time_period'].unique()

time_slider = html.Div([dcc.Slider(
        min = 0,
        max = len(years)-1,
        step = 1,
        value = len(years)-1,
        marks={
            i: f"{year[:4]}/{year[4:]}"
            for i, year in enumerate(years)
        },
        id = "time-slider")
    ],
    id = "time-slider-container",
    style = {"display":"none"}
)

layout = dbc.Container([
    html.H2("ATTAINMENT"),
    html.P("All state-funded secondary schools."),
    html.Div([
            dbc.Row([dbc.Col(la_dropdown)]),
            html.Br(),
            dbc.Row([dbc.Col(student_dropdown), dbc.Col(measure)])
            ],
            style={'backgroundColor': "#E5ECF6",
                'padding': '10px',
                'width': '100%'}),
    dbc.Row(dbc.Col([
        html.Div(id="att-output"),
        html.Br(),
        time_slider,
        html.Br(),
        ])
    )],
    fluid=True,
)

@callback (Output('time-slider-container','style'),
           Input('student-dropdown', 'value'))

def show_time_slider(student):
    if student == "Sex by ethnicity":
        return {"display":"block"}
    else:
        return {"display":"none"}
    
@callback(Output('att-output', 'children'),
          [Input("la-dropdown", "value"), 
           Input("student-dropdown", "value"),
           Input("att-measure", "value"),
           Input("time-slider", "value")]
           )

def update_graph(la, student, measure, time):

    selected_time = years[time]

    result = PLOT_FUNCTIONS[student](df_att_combined, student, la, measure, selected_time)

    if student == "Young carer":
        return result

    return dcc.Graph(figure = result)
