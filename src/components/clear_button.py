from dash import html

def clear_button():
    return html.Button('Очистить график', id='clear-button', n_clicks=0, className='clear-button')
