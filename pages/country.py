from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, all_cont
from addit_modules import age_postfix
import plotly.graph_objects as go

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
                html.Div([
                html.H3('Подробная информация о выбранной стране'),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )
    ]),

    html.Br(),

     dbc.Row ([
        dbc.Col([
            html.P('Выберите континент:')
        ],width=2),
        dbc.Col([
            dcc.Dropdown(
                id = 'crossfilter-cont',
                # заполняем дропдаун уникальными значениями континентоы из датасета
                options = [{'label': i, 'value': i} for i in all_cont],
                # значение континента, выбранное по умолчанию
                value = all_cont[0],
                # возможность множественного выбора
                multi = False
            )
        ],width=3),
        dbc.Col([
            html.P('Выберите страну:')
        ],width=2),
        dbc.Col([
            dcc.Dropdown(
                id = 'crossfilter-count',
                multi = False
            )
        ],width=3)
    ]),


    html.Br(),

        dbc.Row ([
            dbc.Col([
                dbc.Card([
                    dbc.Row([
                        dbc.CardHeader('Уровень жизни')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/money.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='card_text1',
                                className='card-value'),
                            )], width= 8),
                    ])
                ], color = 'success', outline=True, style={'textAlign': 'center'}),
            ],width=3),
            dbc.Col([
                dbc.Card([
                    dbc.Row([
                        dbc.CardHeader('Численность населения')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/religious.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='card_text2',
                                className='card-value'),
                            )], width= 8),
                    ])
                ], color = 'success', outline=True, style={'textAlign': 'center'}),
            ],width=3),
            dbc.Col([
                dbc.Card([
                    dbc.Row([
                        dbc.CardHeader('Образование')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/diploma.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='card_text3',
                                className='card-value'),
                            )], width= 8),
                    ])
                ], color = 'success', outline=True, style={'textAlign': 'center'}),
            ],width=3),
            dbc.Col([
                dbc.Card([
                    dbc.Row([
                        dbc.CardHeader('Статус')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/globe.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='card_text4',
                                className='card-value'),
                            )], width= 8),
                    ])
                ], color = 'success', outline=True, style={'textAlign': 'center'}),
            ],width=3)
    ]),

    html.Br(),
   
    dbc.Container([
        dbc.Row ([
            dbc.Col([
                dcc.Graph(id = 'choropleth1', config={'displayModeBar': False})
            ],width=8),
            dbc.Col([
                dbc.Row([
                    dbc.CardBody(id='card1')
                ]),
                dbc.Row([
                    dbc.Container([
                        dbc.Label('Топ-5 стран по ВВП',
                                  style={'color': 'black',
                                         'display': 'block',
                                         'text-align': 'center',
                                         'font-size': '150%'}),
                        dbc.Table(id='table1')
                    ]),
                    
                ])
            ],width=4)
        ]),
    ])
])

@callback(
    [Output('card_text1','children'),
    Output('card_text2','children'),
    Output('card_text3','children'),
    Output('card_text4','children'),
    Output('card1','children'),
    Output('table1','children'),
    Output('choropleth1', 'figure')
    ],
    [Input('crossfilter-count', 'value'),
    Input('crossfilter-cont', 'value'),
    ]
)

def update_card(count, cont):
    df_count=df[(df['Country'] == count)&(df['Year'] == 2015)]
    df_count14=df[(df['Country'] == count)&(df['Year'] == 2014)]
    gdp_count=df[(df['continent'] == cont)&(df['Year'] == 2015)].sort_values(by='GDP', ascending=False)

    ct1=str(df_count.iloc[0]['Life expectancy']) + ' ' + age_postfix(df_count.iloc[0]['Life expectancy'])
    ct2=str(df_count.iloc[0]['Population']/10).split('.')[0] + ' ' + 'тыс чел.'
    ct3=str(df_count.iloc[0]['Schooling']) + ' ' + age_postfix(df_count.iloc[0]['Schooling'])
    ct4=df_count.iloc[0]['Status']
    gdp15=df_count.iloc[0]['GDP']
    gdp14=df_count14.iloc[0]['GDP']
    gdp_table=gdp_count.iloc[0:5][['Country','GDP']]
    delta_gdp=round((gdp15-gdp14)/gdp14, 2)*100

    fig = go.Figure(
        go.Indicator(
            mode='delta',
            value=gdp15,
            delta={'reference': gdp14, 'relative': True},
            align='center'
        )
    )
    fig.update_layout(margin=dict(l=160, r=0, t=0, b=0)),
    
    card1 = dbc.Card([
        dbc.Row([
            dbc.CardHeader('Валовый внутренний продукт'),    
        ]),
        dbc.Row([
            html.Div([
                html.H3(gdp15),
                html.Div([
                    html.Div([
                        dcc.Graph(figure=fig, style={'height': 50,
                                                     'widht': 100,
                                                     'position': 'relative',
                                                     'justify-content': 'center',
                                                     'align-items': 'center'})
                    ], style={'justify-content': 'center', 'align-items': 'center'}),
                ], style={'text-align': 'center'}),
                html.I(' в % к 2014 году'),
            ])
        ],)
    ], style={'textAlign': 'center'})
    
    table = dbc.Table.from_dataframe(
        gdp_table, striped=True, bordered=True, hover=True, index=False)
    
    figure = px.choropleth(
        gdp_count,
        locations='Country',
        locationmode = 'country names',
        color='GDP',
        hover_name='Country',
        hover_data = {'Country':True,'Year':False,'Status':False,
                    'Life expectancy':True,'Population':True,
                    'GDP':True,'Schooling':False,
                    'continent':False},
        labels={'Country':'Страна', 'Year':'Год',
                'Population':'Население', 'Life expectancy':'Продолжительность жизни',
                'GDP':'ВВП', 'Schooling':'Продолжительность обучения'},
        color_continuous_scale=px.colors.sequential.Pinkyl,
        )
   
    figure.update_layout(margin={'r':0,'t':0,'l':0,'b':0},
                        showlegend=False,
                        coloraxis_showscale=False)


    return ct1, ct2, ct3, ct4, card1, table, figure

@callback(
    [Output('crossfilter-count', 'options'),
    Output('crossfilter-count', 'value'),
    ],
    Input('crossfilter-cont', 'value')
)
def update_region(cont):
    all_count=df[(df['continent'] == cont)]['Country'].unique()
    dd_count = [{'label': i, 'value': i} for i in all_count]
    dd_count_value = all_count[0]
    return dd_count, dd_count_value

