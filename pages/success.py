# %%
################################
######### SUCCESS PAGE #########
################################

import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H2('SUCCESS'),
    html.Div('All success measures will appear here.'),
])
