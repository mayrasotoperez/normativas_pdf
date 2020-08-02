import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'UNTREF - Normativas'
server = app.server # the Flask app


propuestas_lst = os.listdir('assets/normativas')
filtradas = os.listdir('assets/normativas')

niveles = ['Doctorado','Maestría','Especializacion','Diplomatura','Curso']
niveles_dic = {niveles[i] : niveles[i][:3].upper() for i in range(len(niveles))}

app.layout = html.Div([
    html.Div([
        html.H2('Normativas de Posgrado', className='eight columns'),
        html.Img(src='/assets/untref_logo.jpg', className='four columns'),
    ], className='row'),
    html.Hr(className='linea'),

    # SELECCION DE NIVEL
    dcc.RadioItems(
        id='nivel_elegido',
        options=[{'label': niveles[k], 'value': niveles[k][:3].upper()} for k in range(len(niveles))],
        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
        className='niveles',
        value='DOC'
    ),
    html.Hr(className='linea'),

    # DROPDOWN CARRERAS X NIVEL
    html.Div([
        html.Label('Seleccione una propuesta:', className='row'),

        dcc.Dropdown(
                     id='carrera_elegida',
                     clearable=False,
                     ),
    ], className='row'),
    html.Hr(className='linea'),
    # VEMOS EL TÍTULO DE LA CARRERA SELECCIONADA
    html.H5(id='link_title', className='titulo'),

    # AGREGAMOS UN IFRAME PARA VISUALIZAR EL PDF.

    # DROPDOWN CARRERAS X NIVEL
    html.Div([
        html.Label('Seleccione un archivo:', className='row, titulo'),

        dcc.Dropdown(
            id='norma_elegida',
            clearable=False,
            className='titulo',

        ),
    ], className='row'),

    # AQUI DISPONEMOS LAS NORMATIVAS QUE ENCUENTRA
    html.Div(id='tester_div',className='pdf-view'),

],className='cuerpo')

@app.callback(
    Output('carrera_elegida', 'options'),
    [Input('nivel_elegido', 'value')])
def set_nivel(available_options):
    filtradas = []
    for i in propuestas_lst:
        if i.find(available_options) > 0: filtradas.append(i)
    return [dict({'label': filtradas[i], 'value': i}) for i in range(len(filtradas))]

@app.callback(
    Output('link_title', 'children'),
    [Input('nivel_elegido', 'value'),
     Input('carrera_elegida', 'value')])
def set_folder(available_options,carrera):
    filtradas = []
    for i in propuestas_lst:
        if i.find(available_options) > 0: filtradas.append(i)
    try: return filtradas[carrera]
    except: return ''

@app.callback(
    Output('norma_elegida', 'options'),
    [Input('link_title', 'children')])
def set_archivos(norma):

    path = 'assets/normativas/'+norma
    cantidad = len(os.listdir(path))-1
    names = os.listdir(path)
    names.sort()
    if norma == '':
        return [{'label': 'Seleccione una propuesta', 'value': ''}]
    else:
        return [dict({'label': names[i], 'value': names[i]}) for i in range(len(names)-1)]

@app.callback(
    Output('tester_div', 'children'),
    [Input('link_title', 'children'),
     Input('norma_elegida', 'value')])

def show_file(folder,file):
    result = []
    try:
        path = 'assets/normativas/' + folder
        result.append(html.A(className='linkes', children='descargar PDF',
                             href=path + '/' + file,
                             download=''.join(folder.replace('-', '').split(' ')[:3]) + ' --- ' + file),
                      )
        result.append(html.P(file, className='eight columns'),
                      )
        result.append(html.Iframe(src=path + '/' + file, height=600, width=800)
#        result.append(html.Div(html.Iframe(src=path + '/' + file, height=600, width=800),className='titulo')
                      )
    except:
        pass
    if file == '':
        return ''
    else:
        return result


if __name__ == '__main__':
    app.run_server(debug=True)