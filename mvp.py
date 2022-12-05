from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import riskscore as carpreg2

app = Dash(
    __name__,
    title="CardioOb Calc",
    external_stylesheets=[
        dbc.themes.SKETCHY,  # xkcd
        # dbc.themes.PULSE, # fun
        # dbc.themes.VAPOR, # dark
    ],
)

LOGO = app.get_asset_url("logo-PMCC.png")
LOGO = app.get_asset_url("heart.png")


navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Pregnancy + Heart Disease", className="ms-2"
                            )
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            # dbc.Collapse(
            #     search_bar,
            #     id="navbar-collapse",
            #     is_open=False,
            #     navbar=True,
            # ),
        ]
    ),
    color="dark",
    dark=True,
    style={"margin-bottom": "1rem"},
)

carpreg2_dropdown = dcc.Dropdown(
    options=[
        {"label": predictor, "value": predictor} for predictor in carpreg2.predictors
    ],
    multi=True,
)

carpreg2_accordion = html.Div(
    [
        dcc.Markdown(
            """Choose all of the predictors that apply to the patient. As selections are added, the calculated scores will be updated in the adjacent panel"""
        ),
        carpreg2_dropdown,
    ]
)

calculators = html.Div(
    [
        html.H1(
            [
                "CARPREG II ",
                html.A(
                    "(Paper)",
                    href="https://www.jacc.org/doi/abs/10.1016/j.jacc.2018.02.076",
                ),
            ]
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(
                            """### Background:

Identifying women at high risk is an important aspect of care for women with heart disease.

### Objectives:

This study sought to:

1. examine cardiac complications during pregnancy and their temporal trends; and 
2. derive a risk stratification index.

### Methods:
We prospectively enrolled consecutive pregnant women with heart disease and determined their cardiac outcomes during pregnancy. Temporal trends in complications were examined. A multivariate analysis was performed to identify predictors of cardiac complications and these were incorporated into a new risk index.

### Results:
In total, 1,938 pregnancies were included. Cardiac complications occurred in 16% of pregnancies and were primarily related to arrhythmias and heart failure. Although the overall rates of cardiac complications during pregnancy did not change over the years, the frequency of pulmonary edema decreased (8% from 1994 to 2001 vs. 4% from 2001 to 2014; p value = 0.012). Ten predictors of maternal cardiac complications were identified: 5 general predictors (prior cardiac events or arrhythmias, poor functional class or cyanosis, high-risk valve disease/left ventricular outflow tract obstruction, systemic ventricular dysfunction, no prior cardiac interventions); 4 lesion-specific predictors (mechanical valves, high-risk aortopathies, pulmonary hypertension, coronary artery disease); and 1 delivery of care predictor (late pregnancy assessment). These 10 predictors were incorporated into a new risk index (CARPREG II [Cardiac Disease in Pregnancy Study]).

### Conclusions:
Pregnancy in women with heart disease continues to be associated with significant morbidity, although mortality is rare. Prediction of maternal cardiac complications in women with heart disease is enhanced by integration of general, lesion-specific, and delivery of care variables."""
                        )
                    ],
                    title="Abstract",
                ),
                dbc.AccordionItem(
                    [html.Img(src=app.get_asset_url("carpregii-illustration.jpg"))],
                    title="Central Illustration",
                ),
                dbc.AccordionItem(
                    [
                        dcc.Markdown(
                            """Better understand the risk predictors and what they mean"""
                        ),
                        dcc.Graph(figure=carpreg2.predictors_figure),
                    ],
                    title="Risk Predictors",
                ),
                dbc.AccordionItem(
                    [carpreg2_accordion], item_id="carpregii-calc", title="Calculator"
                ),
            ],
            active_item="carpregii-calc",
        ),
    ]
)

empty_figure = px.bar().update_layout(
    annotations=[
        go.layout.Annotation(
            text="X",
            font=go.layout.annotation.Font(size=150),
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
        )
    ]
)

results = html.Div(
    [
        dbc.Row(dbc.Col(html.H1("Results"))),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        [html.H2("Score: "), html.H2("0", id="score")],
                        style={"display": "inline-flex"},
                    )
                ),
                dbc.Col(
                    dbc.Button(
                        [html.H2("Risk: "), html.H2("0%", id="risk-pct")],
                        style={"display": "inline-flex"},
                    )
                ),
            ],
            justify="center",
            align="center",
            class_name="text-center",
        ),
        dbc.Row(dbc.Col(dcc.Graph(figure=empty_figure))),
    ]
)

app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(calculators, sm=12, md=6, class_name="mb-4"),
                        dbc.Col(results, sm=12, md=6),
                    ]
                ),
            ]
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
else:  # running in Gunicorn / on Heroku
    server = app.server
