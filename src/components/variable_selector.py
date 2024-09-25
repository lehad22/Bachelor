from dash import dcc
from dash import html

def variable_selector():
    return html.Div([
        html.Label("Выберите переменную:", className='variable-selector'),
        dcc.Dropdown(
            id='variable-dropdown',
            options=[],
            value=''
        ),
        html.Button('Обновить график', id='update-button', n_clicks=0, className='update-button')
    ],
    className='variable-selector')
