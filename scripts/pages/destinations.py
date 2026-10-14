# %%
#################################
####### DESTINATIONS PAGE #######
#################################

import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H2('DESTINATIONS'),
    html.Div('All destinations measures will appear here.'),
])