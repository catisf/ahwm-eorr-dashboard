# %%
################################
######### SUCCESS PAGE #########
################################

import dash
from dash import html

dash.register_page(__name__,
                   path="/")

layout = html.Div([
    html.H2('HOME'),
    html.Div('About the regional risk register.'),
    html.Br(),
    html.P("Blurb about the risk register, the background of it, how to use it, etc.")
])
