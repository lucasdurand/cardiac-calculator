from dash import html, dcc, Dash, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from more_itertools import always_iterable

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
    id="carpreg2-predictor-dropdown",
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


def create_card(
    text: str,
    *,
    header: str = None,
    title: str = None,
    color: str = "primary",
    outline: bool = True,
) -> dbc.Card:
    return dbc.Card(
        [
            dbc.CardHeader(header) if header else "",
            dbc.CardBody(
                [
                    html.H4("Interpretation", className="card-title") if title else "",
                    html.P(text, className="card-text"),
                ]
            ),
        ],
        color=color,
        outline=outline,
    )


results = html.Div(
    [
        dbc.Row(dbc.Col(html.H1("Your Results"))),
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
            class_name="text-center mb-3",
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H3("Predictors"),
                    html.P(id="predictors-list"),
                ]
            )
        ),
        dbc.Row(dbc.Col([html.Div(id="interpretation-card")])),
        dbc.Row(
            dbc.Col(
                [
                    dcc.Graph(
                        figure=empty_figure.update_layout(
                            title="This Figure Could Show Something?"
                        )
                    )
                ]
            )
        ),
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
                        dbc.Col(
                            results, sm=12, md=6
                        ),  # maybe this is all in a big card that's callbacked to update pieces like color + headers?
                    ]
                ),
            ]
        ),
    ]
)


@callback(
    output=dict(
        results=dict(
            score=Output("score", "children"), risk_pct=Output("risk-pct", "children")
        ),
        interpretation_card=Output("interpretation-card", "children"),
        predictors_list=Output("predictors-list", "children"),
    ),
    inputs=dict(predictors=Input("carpreg2-predictor-dropdown", "value")),
)
def update_scores(predictors):
    predictors_list = html.Ul(
        children=[html.Li(predictor) for predictor in predictors or [None]]
    )
    score = carpreg2.calculate_risk_score(factors=predictors)
    risk_pct = carpreg2.calculate_risk_percentage(score=score)

    match score:
        case score if score == 0:
            color = "success"
            card_header = "Don't worry, be happy"
            card_text = "You're Great!"
        case score if score < 4:
            color = "warning"
            card_header = "Moderate Risk"
            card_text = "You may want to consult a specialist about the potential risks of pregnancy"
        case _:
            color = "danger"
            card_header = "High Risk"
            card_text = (
                "Please consult a specialist about the considerable risks of pregnancy"
            )

    interpretation_card = (
        create_card(
            text=card_text, header=card_header, title="Interpretation", color=color
        ),
    )
    results = dict(score=score, risk_pct=f"{risk_pct:.0%}")

    return dict(
        results=results,
        interpretation_card=interpretation_card,
        predictors_list=predictors_list,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
else:  # running in Gunicorn / on Heroku
    server = app.server
