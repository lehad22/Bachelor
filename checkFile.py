import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import plotly.graph_objs as go
import base64
import netCDF4 as nc
from dash.exceptions import PreventUpdate
import xarray as xr
import numpy as np
import plotly.io as pio
from io import BytesIO

# Создание приложения Dash с использованием темы Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def upload_component(id):
    return dcc.Upload(
        id=id,
        children=dbc.Button("Перетащите или выберите файл", color="primary", outline=True, className="m-2"),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Анализ и Визуализация данных", className="text-center m-4"))
    ]),
    dbc.Row([
        dbc.Col(upload_component('upload-data'), width=6),
        dbc.Col(upload_component('upload-data2'), width=6)
    ]),
    dbc.Row([
        dbc.Col(dbc.Button('Визуализировать', id='submit-button', n_clicks=0, color="success", className='m-2'), width=6),
        dbc.Col(dbc.Button('Очистить график', id='clear-button', n_clicks=0, color="danger", className='m-2'), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='variable-dropdown', placeholder="Выберите переменную"), width=6),
        dbc.Col(dcc.Dropdown(id='variable-dropdown2', placeholder="Выберите переменную"), width=6)
    ]),
    dbc.Col([
        dbc.Col(dbc.Input(id='xaxis-title-input', placeholder='Название оси X', className='m-2'), width=6),
        dbc.Col(dbc.Input(id='yaxis-title-input', placeholder='Название оси Y', className='m-2'), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='output-graph1', style={'display': 'none'}, config={'displaylogo': False}), width=12),
        dbc.Col(dcc.Graph(id='output-graph2', style={'display': 'none'}, config={'displaylogo': False}), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Скачать график"),
                dbc.CardBody([
                    html.Label("Формат:"),
                    dcc.Dropdown(
                        id='format-dropdown',
                        options=[
                            {'label': 'PNG', 'value': 'png'},
                            {'label': 'JPEG', 'value': 'jpeg'},
                            {'label': 'SVG', 'value': 'svg'},
                            {'label': 'PDF', 'value': 'pdf'}
                        ],
                        value='png',
                        className='m-2'
                    ),
                    html.Label("DPI:"),
                    dbc.Input(id='dpi-input', type='number', placeholder='Укажите DPI', value=100, className='m-2'),
                    dbc.Button('Скачать график', id='download-button', n_clicks=0, color="info", className='m-2')
                ])
            ], className='m-2', style={'width': '18rem'})
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Информация о первом файле"),
                dbc.CardBody(html.Div(id='file-info', className='m-2'))
            ], className='m-2')
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Информация о втором файле"),
                dbc.CardBody(html.Div(id='file-info2', className='m-2'))
            ], className='m-2')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Статистика для первого файла"),
                dbc.CardBody([
                    dbc.Button('Показать среднее значение', id='mean-button1', n_clicks=0, className='m-2'),
                    dbc.Button('Показать медиану', id='median-button1', n_clicks=0, className='m-2'),
                    dbc.Button('Показать стандартное отклонение', id='std-button1', n_clicks=0, className='m-2'),
                    html.Div(id='statistics-output1', className='m-2')
                ])
            ], className='m-2')
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Статистика для второго файла"),
                dbc.CardBody([
                    dbc.Button('Показать среднее значение', id='mean-button2', n_clicks=0, className='m-2'),
                    dbc.Button('Показать медиану', id='median-button2', n_clicks=0, className='m-2'),
                    dbc.Button('Показать стандартное отклонение', id='std-button2', n_clicks=0, className='m-2'),
                    html.Div(id='statistics-output2', className='m-2')
                ])
            ], className='m-2')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Информация о переменной (первый файл)"),
                dbc.CardBody(html.Div(id='variable-info', className='m-2'))
            ], className='m-2')
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Информация о переменной (второй файл)"),
                dbc.CardBody(html.Div(id='variable-info2', className='m-2'))
            ], className='m-2')
        ], width=6)
    ]),
    dcc.Download(id='download-graph')
], fluid=True)


def save_uploaded_file(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    with open(filename, 'wb') as f:
        f.write(decoded)


@app.callback(
    Output('download-graph', 'data'),
    Input('download-button', 'n_clicks'),
    State('output-graph1', 'figure'),
    State('format-dropdown', 'value'),
    State('dpi-input', 'value')
)
def download_figure(n_clicks, figure, format, dpi):
    if n_clicks > 0:
        img_bytes = BytesIO()
        pio.write_image(figure, file=img_bytes, format=format, scale=dpi / 72)
        img_bytes.seek(0)
        return dcc.send_bytes(img_bytes.getvalue(), f"graph.{format}")
    raise PreventUpdate


@app.callback(
    Output('statistics-output1', 'children'),
    Input('mean-button1', 'n_clicks'),
    Input('median-button1', 'n_clicks'),
    Input('std-button1', 'n_clicks'),
    State('variable-dropdown', 'value'),
    State('upload-data', 'filename')
)
def display_selected_statistic1(mean_clicks, median_clicks, std_clicks, selected_variable, filename):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.Div()
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'mean-button1':
        statistic_value = 'Среднее значение'
        statistic_func = np.mean
    elif button_id == 'median-button1':
        statistic_value = 'Медиана'
        statistic_func = np.median
    elif button_id == 'std-button1':
        statistic_value = 'Стандартное отклонение'
        statistic_func = np.std
    else:
        return html.Div()

    if selected_variable and filename:
        ds = xr.open_dataset(filename)
        var_data = ds[selected_variable].values
        statistic_result = statistic_func(var_data)
        statistic_info = html.Div([
            html.H4(f"{statistic_value} для переменной {selected_variable} из первого файла:"),
            html.P(f"{statistic_value}: {statistic_result}")
        ])
        return statistic_info
    return html.Div()


@app.callback(
    Output('statistics-output2', 'children'),
    Input('mean-button2', 'n_clicks'),
    Input('median-button2', 'n_clicks'),
    Input('std-button2', 'n_clicks'),
    State('variable-dropdown2', 'value'),
    State('upload-data2', 'filename')
)
def display_selected_statistic2(mean_clicks, median_clicks, std_clicks, selected_variable, filename):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.Div()
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'mean-button2':
        statistic_value = 'Среднее значение'
        statistic_func = np.mean
    elif button_id == 'median-button2':
        statistic_value = 'Медиана'
        statistic_func = np.median
    elif button_id == 'std-button2':
        statistic_value = 'Стандартное отклонение'
        statistic_func = np.std
    else:
        return html.Div()

    if selected_variable and filename:
        ds = xr.open_dataset(filename)
        var_data = ds[selected_variable].values
        statistic_result = statistic_func(var_data)
        statistic_info = html.Div([
            html.H4(f"{statistic_value} для переменной {selected_variable} из второго файла:"),
            html.P(f"{statistic_value}: {statistic_result}")
        ])
        return statistic_info
    return html.Div()


@app.callback(
    Output('file-info', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def display_file_info(contents, filename):
    if contents is not None:
        save_uploaded_file(contents, filename)
        ds = nc.Dataset(filename)
        variable_names = list(ds.variables.keys())
        variables_info = html.Ul([html.Li(var_name) for var_name in variable_names])
        file_info = html.Div([
            html.H5(f"Имя файла: {filename}"),
            html.H6("Переменные:"),
            variables_info,
            html.H6("Глобальные атрибуты:"),
            html.Ul([html.Li(attr) for attr in ds.ncattrs()])
        ])
        return file_info
    return []


@app.callback(
    Output('file-info2', 'children'),
    Input('upload-data2', 'contents'),
    State('upload-data2', 'filename')
)
def display_file_info2(contents, filename):
    if contents is not None:
        save_uploaded_file(contents, filename)
        ds = nc.Dataset(filename)
        variable_names = list(ds.variables.keys())
        variables_info = html.Ul([html.Li(var_name) for var_name in variable_names])
        file_info = html.Div([
            html.H5(f"Имя файла: {filename}"),
            html.H6("Переменные:"),
            variables_info,
            html.H6("Глобальные атрибуты:"),
            html.Ul([html.Li(attr) for attr in ds.ncattrs()])
        ])
        return file_info
    return []


@app.callback(
    Output('variable-dropdown', 'options'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_variable_dropdown(contents, filename):
    if contents is not None:
        save_uploaded_file(contents, filename)
        ds = nc.Dataset(filename)
        variables = list(ds.variables.keys())
        options = [{'label': var, 'value': var} for var in variables]
        return options
    return []


@app.callback(
    Output('variable-dropdown2', 'options'),
    Input('upload-data2', 'contents'),
    State('upload-data2', 'filename')
)
def update_variable_dropdown2(contents, filename):
    if contents is not None:
        save_uploaded_file(contents, filename)
        ds = nc.Dataset(filename)
        variables = list(ds.variables.keys())
        options = [{'label': var, 'value': var} for var in variables]
        return options
    return []


@app.callback(
    Output('variable-info', 'children'),
    Input('variable-dropdown', 'value'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def display_variable_info(selected_variable, contents, filename):
    if contents is not None and selected_variable:
        save_uploaded_file(contents, filename)
        ds = nc.Dataset(filename)
        var = ds.variables[selected_variable]
        info = html.Div([
            html.H5(f"Информация о переменной {selected_variable}:"),
            html.P(f"Название: {var.long_name if 'long_name' in var.ncattrs() else 'Не указано'}"),
            html.P(f"Описание: {var.description if 'description' in var.ncattrs() else 'Нет описания'}"),
            html.P(f"Единицы измерения: {var.units if 'units' in var.ncattrs() else 'Не указаны'}")
        ])
        return info
    return html.Div()


@app.callback(
    Output('variable-info2', 'children'),
    Input('variable-dropdown2', 'value'),
    State('upload-data2', 'contents'),
    State('upload-data2', 'filename')
)
def display_variable_info2(selected_variable, contents, filename):
    if contents is not None and selected_variable:
        save_uploaded_file(contents, filename)
        ds = nc.Dataset(filename)
        var = ds.variables[selected_variable]
        info = html.Div([
            html.H5(f"Информация о переменной {selected_variable}:"),
            html.P(f"Название: {var.long_name if 'long_name' in var.ncattrs() else 'Не указано'}"),
            html.P(f"Описание: {var.description if 'description' in var.ncattrs() else 'Нет описания'}"),
            html.P(f"Единицы измерения: {var.units if 'units' in var.ncattrs() else 'Не указаны'}")
        ])
        return info
    return html.Div()


@app.callback(
    Output('output-graph1', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('xaxis-title-input', 'value'),
    State('yaxis-title-input', 'value')
)
def update_graph1(n_clicks, contents, filename, xaxis_title_user, yaxis_title_user):
    if n_clicks > 0 and contents is not None:
        ds = xr.open_dataset(filename)
        variable_name = list(ds.data_vars)[0]
        var = ds[variable_name]

        xaxis_title = xaxis_title_user if xaxis_title_user else var.dims[2]
        yaxis_title = yaxis_title_user if yaxis_title_user else var.dims[1]
        units = var.attrs.get('units', '')

        x_values = var[var.dims[2]].values
        y_values = var[var.dims[1]].values
        z_values = var.isel(time=0).values
        fig = go.Figure(
            data=go.Heatmap(z=z_values, x=x_values, y=y_values, colorbar={"title": f"Единицы измерения ({units})"}))
        fig.update_layout(title=var.long_name, xaxis_title=xaxis_title, yaxis_title=yaxis_title)
        fig.update_layout(width=1200, height=600)

        return fig
    return {}


@app.callback(
    Output('output-graph2', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('variable-dropdown2', 'value'),
    State('upload-data2', 'contents'),
    State('upload-data2', 'filename'),
    State('xaxis-title-input', 'value'),
    State('yaxis-title-input', 'value')
)
def update_graph2(n_clicks, selected_variable, contents, filename, xaxis_title_user, yaxis_title_user):
    if n_clicks > 0 and contents is not None and selected_variable:
        ds = xr.open_dataset(filename)
        var = ds[selected_variable]

        xaxis_title = xaxis_title_user if xaxis_title_user else var.dims[2]
        yaxis_title = yaxis_title_user if yaxis_title_user else var.dims[1]
        units = var.attrs.get('units', '')
        x_values = var[var.dims[2]].values
        y_values = var[var.dims[1]].values
        z_values = var.isel(time=0).values
        fig = go.Figure(
            data=go.Heatmap(z=z_values, x=x_values, y=y_values, colorbar={"title": f"Единицы измерения ({units})"}))
        fig.update_layout(title=var.long_name, xaxis_title=xaxis_title, yaxis_title=yaxis_title)
        fig.update_layout(width=1200, height=600)

        return fig
    return {}


@app.callback(
    [Output('output-graph1', 'style'),
     Output('output-graph2', 'style')],
    Input('submit-button', 'n_clicks')
)
def show_graph(n_clicks):
    if n_clicks > 0:
        return {'display': 'block'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)
