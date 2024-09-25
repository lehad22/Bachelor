from dash import html, dcc
from src.components.upload_component import upload_component

def create_layout():
    return html.Div([
        html.H1("Визуализация переменной из файлов NetCDF", className="title"),
        upload_component('upload-data'),
        upload_component('upload-data2'),
        html.Button('Визуализировать', id='submit-button', n_clicks=0, className='update-button'),
        html.Button('Очистить график', id='clear-button', n_clicks=0, className='update-button'),
        html.Div(id='variable-dropdown-container', className='variable-selector'),
        html.Div(id='variable-dropdown-container2', className='variable-selector'),
        dcc.Graph(id='output-graph1', style={'display': 'none'}, config={'displaylogo': False}),
        dcc.Graph(id='output-graph2', style={'display': 'none'}, config={'displaylogo': False}),
        html.Div(id='variable-info'),
        html.Div(id='variable-info2'),
        html.Div(id='file-info'),
        html.Div(id='file-info2'),
        html.Button('Показать среднее значение (Файл 1)', id='mean-button1', n_clicks=0, className='update-button'),
        html.Button('Показать медиану (Файл 1)', id='median-button1', n_clicks=0, className='update-button'),
        html.Button('Показать стандартное отклонение (Файл 1)', id='std-button1', n_clicks=0, className='update-button'),
        html.Div(id='statistics-output1'),
        html.Button('Показать среднее значение (Файл 2)', id='mean-button2', n_clicks=0, className='update-button'),
        html.Button('Показать медиану (Файл 2)', id='median-button2', n_clicks=0, className='update-button'),
        html.Button('Показать стандартное отклонение (Файл 2)', id='std-button2', n_clicks=0, className='update-button'),
        html.Div(id='statistics-output2')
    ])
