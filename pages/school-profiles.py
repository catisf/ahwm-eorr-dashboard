# %%
###################################
######### SCHOOL PROFILES #########
###################################

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from load_data import get_school_data

dash.register_page(__name__)

df_schools_wm, LAs = get_school_data()

la_dropdown = html.Div([
    html.P('Local Authority:'),
    dcc.Dropdown(LAs, 'Sandwell', id='la-dropdown')]
)

layout = dbc.Container([
    html.H2("SCHOOL PROFILES"),
    html.P("All state-funded secondary schools."),
    html.Div([
        dbc.Row([dbc.Col(la_dropdown)])
        ],
        style={
            "backgroundColor": "#E5ECF6",
            "padding": "10px",
            "width": "100%"
        }
    ),
    html.Br(),
    dbc.Row([
        dag.AgGrid(
            id="school-table",
            columnDefs=[
                {"field": col}
                for col in df_schools_wm.columns
            ],
            dashGridOptions={
                "pagination": True,
                "paginationPageSize": 25,},
        )
    ]),
    html.Br(),
    html.P("Provisory data, based on 2024 profiles. Data would need to be updated.")
],
fluid=True)

@callback(Output('school-table', 'rowData'),
          Input("la-dropdown", "value") 
        )

def update_table(selected_la):
    table = df_schools_wm[df_schools_wm["LA"] == selected_la]

    return table.to_dict("records")

