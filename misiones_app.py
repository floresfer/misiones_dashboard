
import base64
import io
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dfake={'promo':["aguardando_datos"], 'cuit':["aguardando_datos"], 'nombre':["aguardando_datos"],
        'provincia':["Aguardando Datos"], 'posicion_arancelaria':["aguardando_datos"],
       'descripcion':["aguardando_datos"]}

# Create DataFrame
dfprimario = pd.DataFrame(dfake)


app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP])
#..............TARJETAS

# card_sales = dbc.Card(
#     dbc.CardBody(
#         [
#             html.H1([html.I(className="bi bi-currency-dollar me-2"), "Empresas"], className="text-nowrap"),
#             html.H3(f"{text}",id="q_empresas_card"),
#             html.Div(
#                 [
#                     html.I("5.8%", className="bi bi-caret-up-fill text-success"),
#                     " vs LY",
#                 ]
#             ),
#         ], className="border-start border-success border-5"
#     ),
#     className="text-center m-4"
# )

card_profit = dbc.Card(
    dbc.CardBody(
        [
            html.H1([html.I(className="bi bi-bank me-2"), "Productos"], className="text-nowrap"),
            html.H3("$8.3M",)
        ], className="border-start border-danger border-5"
    ),
    className="text-center m-4",
)

card_provincias = dbc.Card(
    dbc.CardBody(
        [
            html.H1([html.I(className="bi bi-bank me-2"), "Provincias"], className="text-nowrap"),
            html.H3("15",)
        ], className="border-start border-danger border-5"
    ),
    className="text-center m-4",
)

#.........................................

app.layout = dbc.Container([


    dbc.Row([dbc.Col([html.H1("DASHBOARD - MISIONES")], width=8)], justify="center"),
    html.Br(),
    dbc.Row([dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Click para selecionar ',
            html.A('archivo')
        ]), style={'width': '100%',
                   'height': '60px',
                   'lineHeight': '60px',
                   'borderWidth': '1px',
                   'borderStyle': 'dashed',
                   'borderRadius': '5px',
                   'textAlign': 'center',
                   'margin': '10px'},
        # Allow multiple files to be uploaded
            multiple=False )]),
    #dbc.Row([ dbc.Col(q_empresas_card),  dbc.Col(card_profit),dbc.Col(card_provincias)]),
    html.Div(id='q_empresas'),
    html.Br(),
    html.Div(id='detalle_empresas'),
    html.Br(),
    html.Div(id='q_productos'),
    html.Br(),
    html.Div(id='dprods'),
    html.Br(),
    dbc.Row([dbc.Col([html.H4("Inscriptos por Misión")], width=8)], justify="center"),
    html.Br(),
    dbc.Row([dbc.Col([dcc.Graph(id='datatable-upload-graph', figure={})], width=10)],justify="center"),
    html.Br(),
    dbc.Row([dbc.Col([html.H4("Inscripciones | Distribución Geográfica")], width=8)], justify="center"),
    html.Br(),
    dbc.Row([dbc.Col([dcc.Graph(id='donut', figure={})], width=10)],justify="center"),
    html.Br(),
    dbc.Row([dbc.Col([html.H4("Selección de Tabla y descarga de datos:")], width=8)], justify="center"),
    html.Br(),
    dbc.Row([dbc.Col([dcc.Dropdown(id="area_dropdwn",options=["Consolidado","Servicios","Query"],value="Consolidado",clearable=False)], width=10)], justify="center"),#dropdown area
    html.Br(),
    dbc.Row([dbc.Col([ html.Table(id='table_output',style={'textAlign':'center'})])],justify="center"),#Tabla
    html.Br(),
    html.Br()


    ], fluid=True

)


def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    global dfprimario
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            a = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            a = pd.read_excel(io.BytesIO(decoded), names=['cod._promoción', 'promoción', 'pais', 'cuit', 'nombre', 'razon_social',
            'email', 'web', 'domicilio', 'localidad', 'ciudad', 'provincia',
            'cod._postal', 'telefono', 'tamaño', 'actividad', 'socias',
            'cond._mujeres', 'direc._mujeres', 'logo', 'catalogo',
            'nombre_contacto', 'apellido_contacto', 'email_contacto',
            'telefono_contacto', 'complejo_productivo', 'certificaciones',
            'camaras', 'otras_camaras', 'otras_certificaciones', 'redes_sociales',
            'mercados_de_interes', 'exporta_actualmente?', 'posee_fob',
            'detalles_relevantes', 'contrapartes', 'contrapartes_para_reunirse',
            'contrapartes_para_no_reunirse', 'comentarios', 'posicion_arancelaria',
            'descripcion', 'servicio', 'fecha_inscripcion'])
            # a.columns=a.columns.str.strip().str.lower().str.replace(" ","_")
            # a.email_contacto=a.email_contacto.str.lower()
            print("columns:........................")
            print(a.columns)
            print(a.info())
            a.fillna(method="ffill", inplace=True)
            print(a.head(1))
            a["nombre"]=a["nombre"]+";"
            print(a.head(2))

            a["nombre_contacto"]=a["nombre_contacto"]+" "+a["apellido_contacto"]+"; email: "+a["email_contacto"]+"; cel: "+a["telefono_contacto"].astype("str")
            print(a.head(3))
            a["posicion_arancelaria"]=a.posicion_arancelaria.str.strip()+" "+a.descripcion.str.capitalize()
            print(a.head(4))

            a.rename(columns={"cod._promoción":"promo", "pais":"mercado","nombre_contacto":"datos_contacto","posicion_arancelaria":"productos"}, inplace=True)
            print(a.head(5))

            a.drop(columns=["apellido_contacto", "email_contacto","telefono_contacto", "descripcion"], inplace=True)
            print(a.head(6))

            nuevo=a.mercado.str.split(" - ", expand=True)
            print("nuevo")
            print(nuevo.head())
            a["mercado"]=nuevo[1]
            a["iso2"]=nuevo[0]
            print("veamos como queda")
            print(a.head())



            # a["todo_contacto"]=a['nombre_contacto']+" "+a['apellido_contacto']+" ||"+a['email_contacto']+"; "
            # mapper_cuit_contacto=a.drop_duplicates(subset=["cuit","todo_contacto"]).groupby("cuit")[["todo_contacto"]].sum().to_dict()["todo_contacto"]
            # a.drop(columns=['nombre_contacto','apellido_contacto', 'email_contacto'], inplace=True)
            # a.complejo_productivo=a.complejo_productivo+"; "
            # mapper_cuit_complejo=a.drop_duplicates(subset=["cuit","complejo_productivo"]).groupby("cuit")[["complejo_productivo"]].sum().to_dict()["complejo_productivo"]
            # a["complejos"]=a.cuit.map(mapper_cuit_complejo)
            # a.drop(columns="complejo_productivo", inplace=True)
            dfprimario=a.copy()


    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return a



@app.callback(Output('datatable-upload-graph', 'figure'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
            ],
            prevent_initial_call=True)

def update_graph(contents, filename):
    df = parse_data(contents, filename)
    print("a ver")
    print(df)
    dft=df.copy()
    dfprimario=df.copy()


    print(dft.columns)

    j=dft.drop_duplicates(subset=["promo","nombre"], keep="first").groupby(by=["promo"])[["nombre"]].sum()
    k=dft.drop_duplicates(subset=["promo","cuit"], keep="first").groupby(by="promo")[["cuit"]].count()
    l=pd.merge(j.reset_index(),k.reset_index(), on="promo", how="inner")
    l["promo"]=l["promo"].str[-4:]

    fig = px.bar(l, y='cuit', x='promo', text='cuit',
                 hover_data=["promo"],
                 custom_data=["promo"],
                 labels={"cuit":"Cantidad de inscriptos","promo":"pomoción"},
                 title="Cantidad de Inscriptos por actividad de promoción comercial | Click sobre la Misión de su interés para conocer detalles",
                 height=550,
                 color="promo")
    #fig.update_traces(texttemplate='%{text:.1s}', textposition='outside')
    fig.update_layout(showlegend=False)
    fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=11,
                font_family="Rockwell"
                )
        )
    #fig.update_layout(uniformtext_minsize=3, uniformtext_mode='hide')
    return fig



###################################


# injerto para actualizar tarjeta de nùmero de empresa
@app.callback(

    Output("q_empresas","children"),
    Output("detalle_empresas","children"),
    Output("q_productos","children"),
    Output("dprods","children"),
    Output('donut', 'figure'),

    [Input(component_id='datatable-upload-graph', component_property='clickData')],
    prevent_update_call=False
)




def update_cards(clk_data):
    if clk_data is None:

        dff=dfprimario

        donut=dff.drop_duplicates(subset=["promo", "cuit"], keep="first").groupby(by="provincia", as_index=False)[["cuit"]].count()

        fig2 = px.pie(donut, values='cuit', names='provincia',
                      title='Aguardando datos...',
                      height=550,
                      labels={'provincia':'Provincia ', "cuit":"Cantidad de empresas "},
                      hole=0.4)
        fig2.update_traces(textposition='inside', textinfo='percent+label')



        return "Cantidad de Empresas Inscriptas = " + "Esperando datos...", "Detalle Empresas Inscriptas: "+"Esperando datos...", "Cantidad de Productos registrados= "+"Esperando datos...","Detalle Productos: "+"Esperando datos...", fig2


    else:

        print(f'click data: {clk_data}')
        promo = clk_data['points'][0]['x']
        dff=dfprimario.loc[dfprimario["promo"].str[-4:]==promo]
        dff["nombre"]=dff.nombre.str[:-1]
        print("va dff")
        print(dff.head(5))
        print(dff.columns)
        text=str(len(dff.cuit.unique()))
        qprods=str(len(dff.productos.unique()))
        detalle_empresas="  | ".join(dff.nombre.str.capitalize().unique())
        dfh=dff.productos.str[:40]+"..."
        dprods="; ".join(dfh.unique())
        dff["provincia"]=dff.provincia.str.strip().str.capitalize()

        donut=dff.drop_duplicates(subset=["promo", "cuit"], keep="first").groupby(by="provincia", as_index=False)[["cuit"]].count()

        fig2 = px.pie(donut, values='cuit', names='provincia',
                     title='Distribución Geográfica de empresas inscriptas',
                     height=550,
                     labels={'provincia':'Provincia ', "cuit":"Cantidad de empresas "},
                     hole=0.4)
        fig2.update_traces(textposition='inside', textinfo='percent+label')



        return "Cantidad de Empresas inscriptas = " + f"{text}", "Detalle Empresas inscriptas: "+f"{detalle_empresas}", "Cantidad de Productos Registrados = "+f"{qprods}","Detalle Productos: "+f"{dprods}", fig2




###################################


#---------------------------  TABLE ----------------------------------------




@app.callback(
    Output(component_id='table_output',component_property="children"),
    [Input(component_id='datatable-upload-graph', component_property='clickData'),
    Input('area_dropdwn', 'value')]
)


def actualizar_tabla_mercados(clk_data, area):
    if clk_data is None:

        dffq=dfprimario
        table_mercados = dash_table.DataTable(dffq.to_dict("records"),
                             [{"name": i, "id": i} for i in dffq.columns],
                            page_action="none",
                            style_table={"height":"450px","overflowY":"auto"},
                            #fixed_rows={'headers': True},
                            style_data={'whiteSpace': 'normal',
                                         #'backgroundColor': 'rgb(50, 50, 50)',
                                         #'color': 'white',
                                         'height': 'auto',
                                         'lineHeight': '15px'},
                            style_header={#'backgroundColor': 'rgb(30, 30, 30)',
                                         #'color': 'white',
                                         'fontWeight': 'bold',
                                          "textAlign":"left"},
                            style_cell={"textAlign":"justify", "padding":"10px"},
                            style_as_list_view=True,
                            style_cell_conditional=[
                                        {'if': {'column_id': ''},'width': "12%","textAlign":"left"},
                                        {'if': {'column_id': 'Información de Mercado'}, "width":"87%"}],
                            #page_size=10,
                            export_format="csv"
                             )
        return table_mercados

    else:

        if area=="Consolidado":
            promo = clk_data['points'][0]['x']
            dffq=dfprimario.loc[dfprimario["promo"].str[-4:]==promo]
            def create_mapper(column_a, column_b):
                dx=dffq.copy()
                dx[f"{column_b}"]=dx[f"{column_b}"]+" || "
                mapper=dx.drop_duplicates(subset=[f"{column_a}",f"{column_b}"]).groupby(by=f"{column_a}")[[f"{column_b}"]].sum()
                mapper=mapper[f"{column_b}"].str[:-4].to_dict()
                return mapper
            mapper_promo_mercado=create_mapper("promo","mercado")
            mapper_cuit_mercado=create_mapper("cuit","mercado")
            mapper_cuit_contacto=create_mapper("cuit","datos_contacto")
            mapper_cuit_complejo=create_mapper("cuit","complejo_productivo")
            mapper_cuit_producto=create_mapper("cuit","productos")
            mapper_cuit_certificaciones=create_mapper("cuit","certificaciones")
            mapper_cuit_servicio=create_mapper("cuit","servicio")
            mapper_cuit_contrapartes=create_mapper("cuit","contrapartes")
            mapper_cuit_otras_camaras=create_mapper("cuit","otras_camaras")

            dffq.mercado=dffq.promo.map(mapper_promo_mercado)
            dffq.productos=dffq.cuit.map(mapper_cuit_producto)
            dffq.datos_contacto=dffq.cuit.map(mapper_cuit_contacto)
            dffq.complejo_productivo=dffq.cuit.map(mapper_cuit_complejo)
            dffq.servicio=dffq.cuit.map(mapper_cuit_servicio)
            dffq.contrapartes=dffq.cuit.map(mapper_cuit_contrapartes)
            dffq.otras_camaras=dffq.cuit.map(mapper_cuit_otras_camaras)
            dffq.certificaciones=dffq.cuit.map(mapper_cuit_certificaciones)
            dffq.mercado=dffq.cuit.map(mapper_cuit_mercado)


            dffq.drop_duplicates(subset=["promo","cuit"], inplace=True)

            dffq=dffq[['promo','mercado','nombre',"cuit",
                   'email', 'web','ciudad', 'provincia',
                   'telefono','datos_contacto',
                   'complejo_productivo', 'certificaciones', 'camaras', 'otras_camaras',
                   'otras_certificaciones','detalles_relevantes',
                   'contrapartes', 'contrapartes_para_reunirse',
                   'contrapartes_para_no_reunirse', 'comentarios', 'productos', 'servicio',
                   'fecha_inscripcion']]

            table_mercados = dash_table.DataTable(dffq.to_dict("records"),
                                     [{"name": i, "id": i} for i in dffq.columns],
                                    page_action="native",
                                    page_current=0,
                                    page_size=10,
                                    style_table={"height":"500px","width":"1500px","overflowY":"auto", "overflowX":"auto"},
                                    fixed_rows={'headers': True},
                                    style_header={'backgroundColor': 'rgb(30, 30, 30)',
                                                  'textAlign':"left",
                                                  'color': 'white',
                                                  'overflow': 'hidden',
                                                  'textOverflow': 'ellipsis',
                                                  #'maxWidth': 0,
                                                  'fontWeight': 'bold',
                                                  "height":"auto",
                                                  'border': '3px solid pink'},#opcion "auto"

                                    style_cell={'minWidth': 95, 'maxWidth': 300, 'width':"auto"},
                                    style_data={'whiteSpace': 'normal',
                                                'overflow': 'hidden',
                                                'textOverflow': 'ellipsis',
                                                #'maxWidth': 0,
                                                'height': 'auto',
                                                'textAlign':"left",
                                                'border': '2px solid pink'},

                                    export_format="xlsx"
                                     )
            return table_mercados
        elif area=="Query":
            promo = clk_data['points'][0]['x']
            dffq=dfprimario.loc[dfprimario["promo"].str[-4:]==promo]
            table_mercados = dash_table.DataTable(dffq.to_dict("records"),
                                     [{"name": i, "id": i} for i in dffq.columns],
                                    page_action="native",
                                    page_current=0,
                                    page_size=10,
                                    style_table={"height":"500px","width":"1500px","overflowY":"auto", "overflowX":"auto"},
                                    fixed_rows={'headers': True},
                                    style_header={'backgroundColor': 'rgb(30, 30, 30)',
                                                  'textAlign':"left",
                                                  'color': 'white',
                                                  'overflow': 'hidden',
                                                  'textOverflow': 'ellipsis',
                                                  #'maxWidth': 0,
                                                  'fontWeight': 'bold',
                                                  "height":"auto",
                                                  'border': '3px solid pink'},#opcion "auto"

                                    style_cell={'minWidth': 95, 'maxWidth': 300, 'width':"auto"},
                                    style_data={'whiteSpace': 'normal',
                                                'overflow': 'hidden',
                                                'textOverflow': 'ellipsis',
                                                #'maxWidth': 0,
                                                'height': 'auto',
                                                'textAlign':"left",
                                                'border': '2px solid pink'},
                                    export_format="xlsx"
                                     )
            return table_mercados
        elif area=="Servicios":
            promo = clk_data['points'][0]['x']
            dffq=dfprimario.loc[dfprimario["promo"].str[-4:]==promo]
            def create_mapper(column_a, column_b):
                dx=dffq.copy()
                dx[f"{column_b}"]=dx[f"{column_b}"]+" || "
                mapper=dx.drop_duplicates(subset=[f"{column_a}",f"{column_b}"]).groupby(by=f"{column_a}")[[f"{column_b}"]].sum()
                mapper=mapper[f"{column_b}"].str[:-4].to_dict()
                return mapper
            mapper_promo_mercado=create_mapper("promo","mercado")
            mapper_cuit_mercado=create_mapper("cuit","mercado")
            mapper_cuit_contacto=create_mapper("cuit","datos_contacto")
            mapper_cuit_complejo=create_mapper("cuit","complejo_productivo")
            mapper_cuit_producto=create_mapper("cuit","productos")
            mapper_cuit_certificaciones=create_mapper("cuit","certificaciones")
            mapper_cuit_servicio=create_mapper("cuit","servicio")
            mapper_cuit_contrapartes=create_mapper("cuit","contrapartes")
            mapper_cuit_otras_camaras=create_mapper("cuit","otras_camaras")

            dffq.mercado=dffq.promo.map(mapper_promo_mercado)
            dffq.productos=dffq.cuit.map(mapper_cuit_producto)
            dffq.datos_contacto=dffq.cuit.map(mapper_cuit_contacto)
            dffq.complejo_productivo=dffq.cuit.map(mapper_cuit_complejo)
            dffq.servicio=dffq.cuit.map(mapper_cuit_servicio)
            dffq.contrapartes=dffq.cuit.map(mapper_cuit_contrapartes)
            dffq.otras_camaras=dffq.cuit.map(mapper_cuit_otras_camaras)
            dffq.certificaciones=dffq.cuit.map(mapper_cuit_certificaciones)
            dffq.mercado=dffq.cuit.map(mapper_cuit_mercado)


            dffq.drop_duplicates(subset=["promo","cuit"], inplace=True)

            dffq=dffq[['promo','mercado','nombre',"cuit",
                   'email', 'web','ciudad', 'provincia',
                   'telefono','datos_contacto',
                   'complejo_productivo', 'certificaciones', 'camaras', 'otras_camaras',
                   'otras_certificaciones','exporta_actualmente?', 'posee_fob', 'detalles_relevantes',
                   'contrapartes', 'contrapartes_para_reunirse',
                   'contrapartes_para_no_reunirse', 'comentarios','servicio',
                   'fecha_inscripcion']]

            table_mercados = dash_table.DataTable(dffq.to_dict("records"),
                                     [{"name": i, "id": i} for i in dffq.columns],
                                    page_action="native",
                                    page_current=0,
                                    page_size=10,
                                    style_table={"height":"500px","width":"1500px","overflowY":"auto", "overflowX":"auto"},
                                    fixed_rows={'headers': True},
                                    style_header={'backgroundColor': 'rgb(30, 30, 30)',
                                                  'textAlign':"left",
                                                  'color': 'white',
                                                  'overflow': 'hidden',
                                                  'textOverflow': 'ellipsis',
                                                  #'maxWidth': 0,
                                                  'fontWeight': 'bold',
                                                  "height":"auto",
                                                  'border': '3px solid pink'},#opcion "auto"

                                    style_cell={'minWidth': 95, 'maxWidth': 300, 'width':"auto"},
                                    style_data={'whiteSpace': 'normal',
                                                'overflow': 'hidden',
                                                'textOverflow': 'ellipsis',
                                                #'maxWidth': 0,
                                                'height': 'auto',
                                                'textAlign':"left",
                                                'border': '2px solid pink'},
                                    export_format="xlsx"
                                     )
            return table_mercados











#
# def actualizar_tabla_mercados(clk_data, area):
#     if clk_data is None:
#
#         dffq=dfprimario
#         table_mercados = dash_table.DataTable(dffq.to_dict("records"),
#                              [{"name": i, "id": i} for i in dffq.columns],
#                             page_action="none",
#                             style_table={"height":"450px","overflowY":"auto"},
#                             #fixed_rows={'headers': True},
#                             style_data={'whiteSpace': 'normal',
#                                          #'backgroundColor': 'rgb(50, 50, 50)',
#                                          #'color': 'white',
#                                          'height': 'auto',
#                                          'lineHeight': '15px'},
#                             style_header={#'backgroundColor': 'rgb(30, 30, 30)',
#                                          #'color': 'white',
#                                          'fontWeight': 'bold',
#                                           "textAlign":"left"},
#                             style_cell={"textAlign":"justify", "padding":"10px"},
#                             style_as_list_view=True,
#                             style_cell_conditional=[
#                                         {'if': {'column_id': ''},'width': "12%","textAlign":"left"},
#                                         {'if': {'column_id': 'Información de Mercado'}, "width":"87%"}],
#                             #page_size=10,
#                             export_format="csv"
#                              )
#         return table_mercados
#
#     else:

        # promo = clk_data['points'][0]['x']
        # dffq=dfprimario.loc[dfprimario["promo"].str[-4:]==promo]
        # a=dffq
        # table_mercados = dash_table.DataTable(dffq.to_dict("records"),
        #                          [{"name": i, "id": i} for i in dffq.columns],
        #                         page_action="none",
        #                         style_table={"height":"400px","width":"1600px","overflowY":"auto"},
        #                         fixed_rows={'headers': True},
        #                         style_data={'whiteSpace': 'normal',
        #                                      #'backgroundColor': 'rgb(50, 50, 50)',
        #                                      #'color': 'white',
        #                                      'height': 'auto',
        #                                      'lineHeight': '10px'},
        #                         style_header={'backgroundColor': 'rgb(30, 30, 30)',
        #                                      'color': 'white',
        #                                      'fontWeight': 'bold',
        #                                       "textAlign":"left"},
        #                         style_cell={"textAlign":"justify", "padding":"2px"},
        #                         style_as_list_view=True,
        #                         style_cell_conditional=[
        #                                     {'if': {'column_id': ''},'width': "12%","textAlign":"left"},
        #                                     {'if': {'column_id': 'Información de Mercado'}, "width":"87%"}],
        #                         page_size=20,
        #                         export_format="xlsx"
        #                          )
        # return table_mercados
#
#
#
#
#


if __name__ == '__main__':
    app.run_server(debug=True)