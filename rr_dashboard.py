
################################
############# APP ##############
################################

# %%
import dash_bootstrap_components as dbc
from dash import Dash, html, page_container

app = Dash(__name__, 
           use_pages=True, 
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.FLATLY])

server = app.server

HEADER_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "right": 0,
    "height": "100px",
    "backgroundColor":"#2c3e50",
    "color": "white",
    "padding": "1rem",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "100px",
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "margin-top": "95px",
    "padding": "2rem 1rem",
}

header = html.Div([
    html.H1("West Midlands Data Dashboard", className="mb-0"),
    html.P("Last updated: 24/09/2026", className="mb-0", style={'textAlign': 'right'})],
    style=HEADER_STYLE,
)

sidebar = html.Div(
    [dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Demographics", href="/demographics", active="exact"),
                dbc.NavLink("Attainment", href="/attainment", active="exact"),
                dbc.NavLink("Destinations", href="/destinations", active="exact"),
                dbc.NavLink("Success", href="/success", active="exact"),
                dbc.NavLink("School profiles", href="/school-profiles", active="exact"),
                dbc.NavLink("About", href="/about", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div(
    [header,
     sidebar,
     html.Div(page_container,
              style = CONTENT_STYLE),])

if __name__ == '__main__':
    app.run(debug = True)

# %%
