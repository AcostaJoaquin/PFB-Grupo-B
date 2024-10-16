import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz
import plotly.express as px

def get_intercambio_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'intercambio_electrico.csv')
    intercambio_data = pd.read_csv(data_path)

    if 'Fecha actualización' in intercambio_data.columns:
        intercambio_data['datetime'] = pd.to_datetime(intercambio_data['Fecha actualización'], format='%d/%m/%Y')
    else:
        st.error("La columna 'Fecha actualización' no se encontró en el CSV.")
        return pd.DataFrame()

    return intercambio_data

def main(selected_time):
    st.title('Datos de Intercambio Eléctrico')
    intercambio_data = get_intercambio_data()

    if intercambio_data.empty:
        st.warning("No hay datos para mostrar.")
        return

    #timezone = pytz.timezone("Europe/Madrid")

    if selected_time == '7 días':
        fecha_limite = datetime.now() - timedelta(days=4444)
    elif selected_time == '14 días':
        fecha_limite = datetime.now() - timedelta(days=4444)
    elif selected_time == '30 días':
        fecha_limite = datetime.now() - timedelta(days=4440)
    #else:
       #fecha_limite = datetime.now() - timedelta(days=5000)

    filtered_intercambio_data = intercambio_data[intercambio_data['datetime'] >= fecha_limite]

    st.dataframe(filtered_intercambio_data)

    fig = px.line(intercambio_data, x = 'Fecha actualización', y = 'Valores', color= 'nombre',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por País y Tipo',
              line_dash='tipo de intercambio',
              markers= True)
    
    st.plotly_chart(fig,use_container_width= True)

    fig_francia = px.line(intercambio_data[intercambio_data['nombre'] == 'Francia'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio Francia',
              line_dash='tipo de intercambio',
              markers= True)
    st.plotly_chart(fig_francia,use_container_width= True)

    fig_portugal = px.line(intercambio_data[intercambio_data['nombre'] == 'Portugal'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por Portugal',
              line_dash= 'tipo de intercambio',
              markers= True)
    st.plotly_chart(fig_portugal,use_container_width=True)

    fig_marruecos = px.line(intercambio_data[intercambio_data['nombre'] == 'Marruecos'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por Marruecos',
              line_dash= 'tipo de intercambio',
              markers= True)
    st.plotly_chart(fig_marruecos,use_container_width=True)

    fig_andorra = px.line(intercambio_data[intercambio_data['nombre'] == 'Andorra'],
              x='Fecha actualización', y='Valores', color='tipo de intercambio',
              line_group='tipo de intercambio',
              title='Evolución de los valores de intercambio por Andorra',
              markers=True,
              line_dash='tipo de intercambio')
    st.plotly_chart(fig_andorra,use_container_width=True)


    fig1 = px.bar(intercambio_data, x = 'nombre', y = 'Valores', color = 'tipo de intercambio',
             title= 'Valor del intercambio por País y Tipo',
             labels= {'Valores' : 'Valor de intercambio', 'nombre' : 'nombre'},
             barmode= 'group')
    
    st.plotly_chart(fig1,use_container_width= True)

    fig2 = px.scatter(intercambio_data, x = 'Valores', y = 'Porcentaje', color = 'nombre',
                 size= 'Porcentaje', hover_name= 'tipo de intercambio',
                 title = 'Relación entre el valor del intercambio y el porcentaje de cambio',
                 size_max= 10)
    
    st.plotly_chart(fig2,use_container_width= True)




    if __name__ == "__main__":
        selected_time = st.selectbox("Selecciona un periodo de tiempo", ['7 días', '14 días', '30 días', 'Sin filtro'])
        main(selected_time)
