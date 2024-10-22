import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz
import plotly.express as px

## MAPAS ##
import folium
from streamlit_folium import st_folium
from folium.plugins import AntPath

def get_intercambio_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'intercambio_electrico.csv')
    print(f"Data path: {data_path}")
    return pd.read_csv(data_path)

def intercambio_app(selected_time):
    st.title('Datos de Intercambio Eléctrico')
    intercambio_data = get_intercambio_data()

    intercambio_data['Fecha actualización'] = pd.to_datetime(intercambio_data['Fecha actualización'], format='%d/%m/%Y').dt.tz_localize(None)

    today = pd.to_datetime(intercambio_data['Fecha actualización'].iloc[-1]).tz_localize('UTC')
    if selected_time == '7 días':
        date_limit = today - timedelta(days=7)
    elif selected_time == '14 días':
        date_limit = today - timedelta(days=14)
    elif selected_time == '30 días':
        date_limit = today - timedelta(days=30)

    date_limit = date_limit.tz_localize(None)

    filtered_data = intercambio_data[intercambio_data['Fecha actualización'] >= date_limit]

    ##IMPUT DEL TIPO DE INFORMACIÓN DESEADA.
    bar_opciones = ['Importación', 'Exportación', 'saldo']
    selected_option = st.selectbox('Tipo de energía', bar_opciones)


    #Creamos mapa base:
    españa_alt = 40.4637
    españa_lat = -3.7492

    #Creacion del mapa

    from IPython.display import display

    spain_map = folium.Map(location = [españa_alt, españa_lat],
                       zoom_start= 5,
                       tiles = 'Esri Worldimagery',
                       width='500px',
                       height='500px'
                       )

    bounds =   [[51.1242, -17.0000],[20.0000, 9.6625]]

    spain_map.fit_bounds(bounds)


    #Coordenadas de los paises donde existe un intercambio energetico.
    lista_paises = ['Marruecos', 'Francia', 'Portugal', 'Andorra', 'España']
    lista_altitudes = [31.83999, 46.57771, 39.68023, 42.5462, 40.4637]
    lista_latitudes = [-6.19721, 2.78159, -8.80606, 1.5034, -3.7492]

    df_coordenadas = pd.DataFrame()
    df_coordenadas['nombre'] = lista_paises
    df_coordenadas['altitud'] = lista_altitudes
    df_coordenadas['latitud'] = lista_latitudes


    #Creacion de variables con sus coordenadas
    marruecos = [df_coordenadas['altitud'][0], df_coordenadas['latitud'][0]]
    francia = [df_coordenadas['altitud'][1], df_coordenadas['latitud'][1]]
    portugal = [df_coordenadas['altitud'][2], df_coordenadas['latitud'][2]]
    andorra = [df_coordenadas['altitud'][3], df_coordenadas['latitud'][3]]
    españa = [df_coordenadas['altitud'][4], df_coordenadas['latitud'][4]]


    #Unión de df_coordenadas y df incluido en la función - en nuestro caso, df_intercambio.
    df_unido = pd.merge(filtered_data, df_coordenadas, how = 'left', on = 'nombre')


    #Creación de iconos por país
    españa_url = "https://upload.wikimedia.org/wikipedia/en/9/9a/Flag_of_Spain.svg"
    españa_icon = folium.CustomIcon(españa_url, icon_size=(50, 30))

    marruecos_url = "https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg"
    marruecos_icon = folium.CustomIcon(marruecos_url, icon_size=(40, 20))

    andorra_url = "https://upload.wikimedia.org/wikipedia/commons/1/19/Flag_of_Andorra.svg"
    andorra_icon = folium.CustomIcon(andorra_url, icon_size=(40, 20))

    francia_url = "https://upload.wikimedia.org/wikipedia/en/c/c3/Flag_of_France.svg"
    francia_icon = folium.CustomIcon(francia_url, icon_size=(40, 20))

    portugal_url = "https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_Portugal.svg"
    portugal_icon = folium.CustomIcon(portugal_url, icon_size=(40, 20))


    ## df_filtrado es el df resultante del tipo de intercambio deseado.
    df_filtrado = df_unido[df_unido['tipo de intercambio'] == selected_option]

    #CREACIÓN DEL MAPA CON INFORMACIÓN
    intercambios = folium.map.FeatureGroup(name='Intercambios')


    for lat, lng, pais, valores, porcentaje, fecha in zip(df_filtrado['altitud'],
                           df_filtrado['latitud'],
                           df_filtrado['nombre'],
                           df_filtrado['Valores'],
                           df_filtrado['Porcentaje'],
                           df_filtrado['Fecha actualización']):

            contenido_label = f'''<b> Pais: {pais} </b><br>
                            <b>Tipo de intercambio: {selected_option} </b><br>
                            <b>Valores: {valores} </b><br>
                            <b>Porcentaje: {porcentaje} </b><br>
                            <b>Fecha actualización: {fecha} </b>'''
            intercambios.add_child(folium.Marker(location=[lat, lng],
                                                 popup=contenido_label))



    spain_map.add_child(intercambios)



    folium.Marker(
          location= españa,
          icon=españa_icon,
          popup = 'España'
          ).add_to(spain_map)

    folium.Marker(
          location= portugal,
          icon=portugal_icon,
          popup = 'Portugal'
          ).add_to(spain_map)
    folium.Marker(
          location= francia,
          icon=francia_icon,
          popup = 'Francia'
          ).add_to(spain_map)
    folium.Marker(
          location= marruecos,
          icon=marruecos_icon,
          popup = 'Marruecos'
          ).add_to(spain_map)
    folium.Marker(
          location= andorra,
          icon=andorra_icon,
          popup = 'Andorra'
          ).add_to(spain_map)


    for i, v in df_filtrado[df_filtrado['nombre'] == 'Francia'].iterrows():
        if v['Valores'] < 0:
                AntPath(locations = [españa, francia],
                color = 'blue',
                delay = 2000,
                weight = 5).add_to(spain_map)
        elif v['Valores'] > 0:
                AntPath(locations = [francia,españa],
                color = 'blue',
                delay = 2000,
                weight = 5).add_to(spain_map)
        else:
                pass

    for i, v in df_filtrado[df_filtrado['nombre'] == 'Andorra'].iterrows():
        if v['Valores'] < 0:
                AntPath(locations = [españa, andorra],
                color = 'orange',
                delay = 2000,
                weight = 5).add_to(spain_map)
        elif v['Valores'] > 0:
                AntPath(locations = [andorra,españa],
                color = 'orange',
                delay = 2000,
                weight = 5).add_to(spain_map)
        else:
                pass

    for i, v in df_filtrado[df_filtrado['nombre'] == 'Marruecos'].iterrows():
        if v['Valores'] < 0:
                AntPath(locations = [españa, marruecos],
                color = 'red',
                delay = 2000,
                weight = 5).add_to(spain_map)
        elif v['Valores'] > 0:
                AntPath(locations = [marruecos, españa],
                color = 'red',
                delay = 2000,
                weight = 5).add_to(spain_map)
        else:
                pass

    for i, v in df_filtrado[df_filtrado['nombre'] == 'Portugal'].iterrows():
        if v['Valores'] < 0:
                AntPath(locations = [españa, portugal],
                color = 'green',
                delay = 2000,
                weight = 5).add_to(spain_map)
        elif v['Valores'] > 0:
                AntPath(locations = [portugal, españa],
                color = 'green',
                delay = 2000,
                weight = 5).add_to(spain_map)
        else:
                pass


    st_folium(spain_map, width=725)


    fig = px.line(df_filtrado, x = 'Fecha actualización', y = 'Valores', color= 'nombre',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por País y Tipo',
              line_dash='tipo de intercambio',
              markers= True)

    st.plotly_chart(fig,use_container_width= True)


    fig_francia = px.line(df_filtrado[df_filtrado['nombre'] == 'Francia'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio Francia',
              line_dash='tipo de intercambio',
              markers= True)
    st.plotly_chart(fig_francia,use_container_width= True)


    fig_portugal = px.line(filtered_data[filtered_data['nombre'] == 'Portugal'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por Portugal',
              line_dash= 'tipo de intercambio',
              markers= True)
    st.plotly_chart(fig_portugal,use_container_width=True)


    fig_marruecos = px.line(df_filtrado[df_filtrado['nombre'] == 'Marruecos'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por Marruecos',
              line_dash= 'tipo de intercambio',
              markers= True)
    st.plotly_chart(fig_marruecos,use_container_width=True)


    fig_andorra = px.line(df_filtrado[df_filtrado['nombre'] == 'Andorra'],
              x='Fecha actualización', y='Valores', color='tipo de intercambio',
              line_group='tipo de intercambio',
              title='Evolución de los valores de intercambio por Andorra',
              markers=True,
              line_dash='tipo de intercambio')
    st.plotly_chart(fig_andorra,use_container_width=True)


    fig1 = px.bar(df_filtrado, x = 'nombre', y = 'Valores', color = 'tipo de intercambio',
             title= 'Valor del intercambio por País y Tipo',
             labels= {'Valores' : 'Valor de intercambio', 'nombre' : 'nombre'},
             barmode= 'group')

    st.plotly_chart(fig1,use_container_width= True)


    fig2 = px.scatter(df_filtrado, x = 'Valores', y = 'Porcentaje', color = 'nombre',
                 size= 'Porcentaje', hover_name= 'tipo de intercambio',
                 title = 'Relación entre el valor del intercambio y el porcentaje de cambio',
                 size_max= 10)

    st.plotly_chart(fig2,use_container_width= True)




    if __name__ == "__main__":
        intercambio_app(selected_time)
