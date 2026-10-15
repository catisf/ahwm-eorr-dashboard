# %%
################################
######### SUCCESS PAGE #########
################################

import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H2('ABOUT'),
    html.Br(),
    html.Div([
        html.H3('Data sources'),
        html.P('The data used in this dashboard is publicly available. This file contains a list of the files used to produce this dashboard and where you can find them.'),
    ]),
    html.Br(),
    html.Br(),
    html.Div([
        html.H3('Understanding the measures'),
        html.Br(),
        html.H5('FSM'),
        html.P('FSM eligible - taking free school meal on census date: This measure represents the percentage of pupils who are eligible for free school meals and actually took a free school meal on the census date.'),
        html.P('FSM eligible -   performance table metric: This measure represents the percentage of pupils who are eligible for free school meals, regardless of whether they took a free school meal on the census date.'),
        html.Br(),       
        html.H5('Attainment 8'),
        html.P('Attainment 8: This measure represents the average attainment score of pupils across 8 subjects at the end of their secondary education.'),
        html.Br(),
        html.H5('Progress 8'),
        html.P('Progress 8: This measure represents the average progress made by pupils in their secondary education, accounting for their prior attainment.'),
    ])
])
