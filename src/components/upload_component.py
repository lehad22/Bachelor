from dash import dcc
from dash import html

def upload_component(id_name):
    return dcc.Upload(
        id=id_name,
        children=html.Div([
            'Перетащите файл сюда или ',
            html.A('выберите файл')
        ]),
        multiple=False, className='upload-data'
    )
