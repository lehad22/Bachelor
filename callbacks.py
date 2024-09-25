import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objs as go
import base64
import netCDF4 as nc
import xarray as xr
import numpy as np
from src.components.upload_component import upload_component


def register_callbacks(app):
    # Все обратные вызовы (callbacks) из вашего исходного кода
    # Например:
    @app.callback(
        Output('statistics-output1', 'children'),
        [Input('mean-button1', 'n_clicks'),
         Input('median-button1', 'n_clicks'),
         Input('std-button1', 'n_clicks')],
        [State('variable-dropdown1', 'value'),
         State('upload-data1', 'filename')]
    )
    def display_selected_statistic1(mean_clicks, median_clicks, std_clicks, selected_variable, filename):
        # Тело функции display_selected_statistic1
        pass

# Функция для вычисления статистических показателей
# Функция для вычисления статистических показателей
def calculate_statistics(data):
    mean_value = np.mean(data)
    median_value = np.median(data)
    std_deviation = np.std(data)
    return mean_value, median_value, std_deviation

# Обратный вызов для отображения статистического показателя по нажатию на кнопку для первого файла
@app.callback(
    Output('statistics-output1', 'children'),
    [Input('mean-button1', 'n_clicks'),
     Input('median-button1', 'n_clicks'),
     Input('std-button1', 'n_clicks')],
    [State('variable-dropdown1', 'value'),
     State('upload-data1', 'filename')]
)
def display_selected_statistic1(mean_clicks, median_clicks, std_clicks, selected_variable, filename):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'mean-button1' in changed_id:
        statistic_value = 'Среднее значение'
        statistic_func = np.mean
    elif 'median-button1' in changed_id:
        statistic_value = 'Медиана'
        statistic_func = np.median
    elif 'std-button1' in changed_id:
        statistic_value = 'Стандартное отклонение'
        statistic_func = np.std
    else:
        return html.Div()

    if selected_variable and filename:
        ds = xr.open_dataset(filename)
        var_data = ds[selected_variable].values
        statistic_result = statistic_func(var_data)
        statistic_info = html.Div([
            html.H3(f"{statistic_value} для переменной {selected_variable} из первого файла:"),
            html.P(f"{statistic_value}: {statistic_result}")
        ])
        return statistic_info
    return html.Div()

# Обратный вызов для отображения статистического показателя по нажатию на кнопку для второго файла
@app.callback(
    Output('statistics-output2', 'children'),
    [Input('mean-button2', 'n_clicks'),
     Input('median-button2', 'n_clicks'),
     Input('std-button2', 'n_clicks')],
    [State('variable-dropdown2', 'value'),
     State('upload-data2', 'filename')]
)
def display_selected_statistic2(mean_clicks, median_clicks, std_clicks, selected_variable, filename):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'mean-button2' in changed_id:
        statistic_value = 'Среднее значение'
        statistic_func = np.mean
    elif 'median-button2' in changed_id:
        statistic_value = 'Медиана'
        statistic_func = np.median
    elif 'std-button2' in changed_id:
        statistic_value = 'Стандартное отклонение'
        statistic_func = np.std
    else:
        return html.Div()

    if selected_variable and filename:
        ds = xr.open_dataset(filename)
        var_data = ds[selected_variable].values
        statistic_result = statistic_func(var_data)
        statistic_info = html.Div([
            html.H3(f"{statistic_value} для переменной {selected_variable} из второго файла:"),
            html.P(f"{statistic_value}: {statistic_result}")
        ])
        return statistic_info
    return html.Div()

# # Обратный вызов для вычисления и отображения статистических данных для первого файла
# @app.callback(
#     Output('statistics-output', 'children'),
#     [Input('variable-dropdown', 'value')],
#     [State('upload-data', 'filename')]
# )
# def display_statistics(selected_variable, filename):
#     if selected_variable and filename:
#         ds = xr.open_dataset(filename)
#         var_data = ds[selected_variable].values
#         mean, median, std = calculate_statistics(var_data)
#         statistics_info = html.Div([
#             html.H3(f"Статистические показатели для переменной {selected_variable} из первого файла:"),
#             html.P(f"Среднее значение: {mean}"),
#             html.P(f"Медиана: {median}"),
#             html.P(f"Стандартное отклонение: {std}")
#         ])
#         return statistics_info
#     return html.Div()
#
# # Обратный вызов для вычисления и отображения статистических данных для второго файла
# @app.callback(
#     Output('statistics-output2', 'children'),
#     [Input('variable-dropdown2', 'value')],
#     [State('upload-data2', 'filename')]
# )
# def display_statistics2(selected_variable, filename):
#     if selected_variable and filename:
#         ds = xr.open_dataset(filename)
#         var_data = ds[selected_variable].values
#         mean, median, std = calculate_statistics(var_data)
#         statistics_info = html.Div([
#             html.H3(f"Статистические показатели для переменной {selected_variable} из второго файла:"),
#             html.P(f"Среднее значение: {mean}"),
#             html.P(f"Медиана: {median}"),
#             html.P(f"Стандартное отклонение: {std}")
#         ])
#         return statistics_info
#     return html.Div()

# Функция для загрузки файла
def save_uploaded_file(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    with open(filename, 'wb') as f:
        f.write(decoded)

# Обратные вызовы для загрузки файлов и отображения информации
@app.callback(
    Output('file-info', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def display_file_info(contents, filename):
    if contents is not None:
        save_uploaded_file(contents, filename)
        ds = nc.Dataset(filename)
        variable_names = list(ds.variables.keys())  # Получаем список названий переменных
        variables_info = html.Ul([html.Li(var_name) for var_name in variable_names])
        file_info = html.Div([
            html.Hr(),
            html.H3("Информация о первом загруженном файле:"),
            html.P(f"Имя файла: {filename}"),
            html.P("Переменные:"),
            variables_info,
            html.P(f"Глобальные атрибуты: {', '.join(ds.ncattrs())}")
        ])
        return [file_info, html.Hr()]  # Добавляем разделитель после каждой информации о файле
    return []

@app.callback(
    Output('file-info2', 'children'),
    [Input('upload-data2', 'contents')],
    [State('upload-data2', 'filename')]
)
def display_file_info2(contents, filename):
    if contents is not None:
        save_uploaded_file(contents, filename)
        ds = nc.Dataset(filename)
        variable_names = list(ds.variables.keys())  # Получаем список названий переменных
        variables_info = html.Ul([html.Li(var_name) for var_name in variable_names])
        file_info = html.Div([
            html.H3("Информация о втором загруженном файле:"),
            html.P(f"Имя файла: {filename}"),
            html.P("Переменные:"),
            variables_info,
            html.P(f"Глобальные атрибуты: {', '.join(ds.ncattrs())}")
        ])
        return [file_info, html.Hr()]  # Добавляем разделитель после каждой информации о файле
    return []


# Определение обратной связи для загрузки файла
@app.callback(
    Output('upload-data', 'contents'),
    [Input('upload-data', 'filename')],
    [State('upload-data', 'contents')]
)
def update_upload(filename, contents):
    if filename is not None:
        return contents

# Определение обратной связи для вывода доступных переменных
@app.callback(
    Output('variable-dropdown-container', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]  # Добавляем состояние для получения имени файла
)
def display_variables(contents, filename):  # Добавляем параметр filename
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        with open(filename, 'wb') as f:  # Используем переданное имя файла
            f.write(decoded)
        ds = nc.Dataset(filename)
        variables = list(ds.variables.keys())
        dropdown = dcc.Dropdown(
            id='variable-dropdown',
            options=[{'label': var, 'value': var} for var in variables],
            value=variables[0]
        )
        return dropdown

# Определение обратной связи для вывода информации о переменной
@app.callback(
    Output('variable-info', 'children'),
    [Input('variable-dropdown', 'value')],
    [State('upload-data', 'contents'),
     State('upload-data', 'filename')]  # Добавляем состояние для получения имени файла
)
def display_variable_info(selected_variable, contents, filename):  # Добавляем параметр filename
    if contents is not None and selected_variable:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        with open(filename, 'wb') as f:  # Используем переданное имя файла
            f.write(decoded)
        ds = nc.Dataset(filename)
        var = ds.variables[selected_variable]
        info = html.Div([
            html.H3(f"Информация о переменной {selected_variable}:"),
            html.P(f"Название: {var.long_name if 'long_name' in var.ncattrs() else 'Не указано'}"),
            html.P(f"Описание: {var.description if 'description' in var.ncattrs() else 'Нет описания'}"),
            html.P(f"Единицы измерения: {var.units if 'units' in var.ncattrs() else 'Не указаны'}")
        ])
        return info
    return html.Div()

# Определение обратной связи для вывода списка всех переменных
@app.callback(
    Output('variable-list', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]  # Добавляем состояние для получения имени файла
)
def display_all_variables(contents, filename):  # Добавляем параметр filename
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        with open(filename, 'wb') as f:  # Используем переданное имя файла
            f.write(decoded)
        ds = nc.Dataset(filename)
        variables = list(ds.variables.keys())
        variable_list = [html.Li(var) for var in variables]
        return variable_list
    return []

# Обратный вызов для визуализации данных из первого файла
@app.callback(
    Output('output-graph1', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('upload-data', 'contents'),
     State('upload-data', 'filename')]
)
def update_graph1(n_clicks, contents, filename):
    if n_clicks > 0 and contents is not None:
        ds = xr.open_dataset(filename)
        # Здесь вы должны выбрать переменную для визуализации, например:
        variable_name = list(ds.data_vars)[0]  # выбираем первую переменную
        var = ds[variable_name]
        fig = go.Figure(data=go.Heatmap(z=var.isel(time=0).values))
        fig.update_layout(title=variable_name, xaxis_title=('degrees_east'), yaxis_title=('degrees_north')) # Сдэлат нормальные оси!!!!!!!!!!!!!
        return fig
    return {}

# Обратный вызов для визуализации данных из второго файла с использованием выбранной переменной
@app.callback(
    Output('output-graph2', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('variable-dropdown2', 'value'),
     State('upload-data2', 'contents'),
     State('upload-data2', 'filename')]
)
def update_graph2(n_clicks, selected_variable, contents, filename):
    if n_clicks > 0 and contents is not None and selected_variable:
        ds = xr.open_dataset(filename)
        var = ds[selected_variable]
        fig = go.Figure(data=go.Heatmap(z=var.isel(time=0).values))
        fig.update_layout(title=selected_variable, xaxis_title=('degrees_east'), yaxis_title=('degrees_north'))
        return fig
    return {}

# Обратный вызов для отображения выпадающего списка переменных для второго файла
@app.callback(
    Output('variable-dropdown-container2', 'children'),
    [Input('upload-data2', 'contents')],
    [State('upload-data2', 'filename')]
)
def display_variables2(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        with open(filename, 'wb') as f:
            f.write(decoded)
        ds = nc.Dataset(filename)
        variables = list(ds.variables.keys())
        dropdown = dcc.Dropdown(
            id='variable-dropdown2',
            options=[{'label': var, 'value': var} for var in variables],
            value=variables[0] if variables else None
        )
        return dropdown

# Обратный вызов для отображения информации о выбранной переменной для второго файла
@app.callback(
    Output('variable-info2', 'children'),
    [Input('variable-dropdown2', 'value')],
    [State('upload-data2', 'contents'),
     State('upload-data2', 'filename')]
)
def display_variable_info2(selected_variable, contents, filename):
    if contents is not None and selected_variable:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        with open(filename, 'wb') as f:
            f.write(decoded)
        ds = nc.Dataset(filename)
        var = ds.variables[selected_variable]
        info = html.Div([
            html.H3(f"Информация о переменной {selected_variable}:"),
            html.P(f"Название: {var.long_name if 'long_name' in var.ncattrs() else 'Не указано'}"),
            html.P(f"Описание: {var.description if 'description' in var.ncattrs() else 'Нет описания'}"),
            html.P(f"Единицы измерения: {var.units if 'units' in var.ncattrs() else 'Не указаны'}")
        ])
        return info
    return html.Div()

# Обратный вызов для отображения графиков после нажатия кнопки
@app.callback(
    [Output('output-graph1', 'style'),
     Output('output-graph2', 'style')],
    [Input('submit-button', 'n_clicks')]
)
def show_graph(n_clicks):
    if n_clicks > 0:
        return {'display': 'block'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'none'}
