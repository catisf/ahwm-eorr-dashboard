# %%
#####################################
######### DEMOGRAPHICS PAGE #########
#####################################

# %%
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_ag_grid as dag
from load_data import get_att_data

# %% Load data
df_att_combined, LAs = get_att_data()

# %%
dash.register_page(__name__)

# Card function
def metric_card(title, value):
    return dbc.Card(
        dbc.CardBody([
            html.H4(
                title,
                className="card-title"
            ),
            html.H2(
                value,
                style={
                    "fontWeight": "bold",
                    "color": "#0B4F9C"
                }
            )
        ]),
        style={
            "textAlign": "center",
            "border": "1px solid #0B4F9C",
            "height": "100%"
        }
    )

# Create LA tabs
la_tabs = dbc.Tabs(
    [
        dbc.Tab(label="National", tab_id="National"),
        dbc.Tab(label="West Midlands", tab_id="West Midlands"),
    ]
    + [
        dbc.Tab(
            label=(
                "Herefordshire"
                if la == "Herefordshire, County of"
                else la
            ),
            tab_id=la,
            tab_style={
                "flex": "0 0 16.666%",
                "textAlign": "center"
            },
        )
        for la in sorted(
            [la for la in LAs if la != "National"]
        )
    ],
    id="la-tabs",
    active_tab="National",
    class_name="la-tabs",
)


# Page layout
layout = html.Div([
    html.H2("DEMOGRAPHIC INFORMATION"),
    html.Br(),
    html.Div([
        la_tabs
    ],
        style={
            "backgroundColor": "#E5ECF6",
            "padding": "10px",
            "width": "100%"
        }
    ),
    html.Br(),
    html.Div(id="demographics-output"),

])


@callback(
    Output("demographics-output", "children"),
    Input("la-tabs", "active_tab")
)

def update_demographics(selected_la):

    # Filter once for LA and year

    if selected_la == "West Midlands":
        la_df = df_att_combined[
        (df_att_combined["la_name"] != "National") &
        (df_att_combined["time_period"] == "202425")
    ]
    else:
        la_df = df_att_combined[
        (df_att_combined["la_name"] == selected_la) &
        (df_att_combined["time_period"] == "202425")
    ]

    # Figures
    total_df = la_df[
        la_df["breakdown_topic"] == "Total"
    ]

    school_count = total_df["school_count"].sum()
    pupil_count = total_df["pupil_count"].sum()

    # FSM
    fsm_df = la_df[
        (la_df["breakdown_topic"] == "FSM status") &
        (la_df["fsm_status"] == "FSM eligible")
    ]

    fsm_count = fsm_df["pupil_count"].sum()

    fsm_percent = (fsm_count / pupil_count * 100)

    # Young carers
    carer_df = la_df[
        (la_df["breakdown_topic"] == "Young carer") &
        (la_df["young_carer"] == "Young carer")
    ]

    carer_count = carer_df["pupil_count"].sum()

    # Sex
    girls_df = la_df[(la_df["breakdown_topic"] == "Sex") &
                     (la_df["sex"] == "Girls")]

    boys_df = la_df[(la_df["breakdown_topic"] == "Sex") &
                     (la_df["sex"] == "Boys")]

    percent_girls = girls_df["pupil_count"].sum()/pupil_count*100
    percent_boys = boys_df["pupil_count"].sum()/pupil_count*100

    # Cards
    cards = [
        metric_card("Number of schools",
                    f"{school_count:,.0f}"),

        metric_card("Number of pupils",
                    f"{pupil_count:,.0f}"),

        metric_card("% eligible for FSM",
                    f"{fsm_percent:.1f}%"),

        metric_card("% Boys",
                    f"{percent_boys:.1f}%"),

        metric_card("% Girls",
                     f"{percent_girls:.1f}%"),
        
        metric_card("Young carers",
                    f"{carer_count:,.0f}")
    ]

    # IMD graph
    #if selected_la == "National":
    #    imd = df_imd
    #elif selected_la == "West Midlands":
    #    imd = df_imd[df_imd['Local Authority District name (2024)'].isin(LAs)]
    #else:
    #    imd = df_imd[df_imd['Local Authority District name (2024)'] == selected_la]

    

    #fig = px.bar(imd,
    #    x='Local Authority District name (2024)',
    #    y='Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOA',
    #    labels={
    #        'Local Authority District name (2024)': 'Local Authority',
    #        'Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOA': 'IMD Decile'
    #    })

    # Ethnicity table
    if selected_la == "West Midlands":
        ethn_df = (
            la_df[la_df["breakdown_topic"] == "Ethnicity"]
            .groupby(
                ["ethnicity_major", "ethnicity_minor"],
                as_index=False
                )["pupil_count"].sum()
        )
    else:
        ethn_df = (la_df[la_df["breakdown_topic"] == "Ethnicity"][["ethnicity_major","ethnicity_minor", "pupil_count"]]
               .sort_values("ethnicity_minor")
               .copy())

    ethn_df["% of pupils"] = (ethn_df["pupil_count"]/ pupil_count* 100).round(1)

    ethn_df["is_total"] = (ethn_df["ethnicity_minor"].str.startswith("All ", na=False))

    ethn_df = ethn_df.sort_values(by=["ethnicity_major", "is_total", "ethnicity_minor"],ascending=[True, False, True])

    ethn_df = ethn_df.rename(columns={"ethnicity_minor": "Ethnicity"})

    ethnicity_table = dag.AgGrid(
        columnDefs=[
            {"field": "Ethnicity",
             "cellStyle":{"styleConditions":[
                 {"condition": "params.data.is_total == true",
                  "style":{"fontWeight": "bold"                  
                  }}
             ]
             }},
            {"field": "% of pupils"}
    ],
    rowData=ethn_df.to_dict("records"),
    defaultColDef={
        "sortable": True,
        "filter": True,
        "resizable": True
    },
    columnSize="sizeToFit",
    dashGridOptions={
        "domLayout": "autoHeight"
    })

    return html.Div([
        html.H3(selected_la),
        html.Br(),
        dbc.Row(
            [dbc.Col(
                    card,
                    xs=12,
                    sm=6,
                    lg=4,
                    class_name="mb-3"
                )
                for card in cards
            ],
            class_name="g-3"
        ),
        html.Br(),
        #html.H4("Index of Multiple Deprivation (IMD)"),
        #dcc.Graph(figure=fig),
        html.H4("Etnicity"),
        ethnicity_table
    ])