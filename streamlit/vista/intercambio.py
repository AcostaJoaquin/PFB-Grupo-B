import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz
import plotly.express as px

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



    fig = px.line(filtered_data, x = 'Fecha actualización', y = 'Valores', color= 'nombre',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por País y Tipo',
              line_dash='tipo de intercambio',
              markers= True)

    st.plotly_chart(fig,use_container_width= True)

    fig_francia = px.line(filtered_data[filtered_data['nombre'] == 'Francia'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
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

    fig_marruecos = px.line(filtered_data[filtered_data['nombre'] == 'Marruecos'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por Marruecos',
              line_dash= 'tipo de intercambio',
              markers= True)
    st.plotly_chart(fig_marruecos,use_container_width=True)

    fig_andorra = px.line(filtered_data[filtered_data['nombre'] == 'Andorra'],
              x='Fecha actualización', y='Valores', color='tipo de intercambio',
              line_group='tipo de intercambio',
              title='Evolución de los valores de intercambio por Andorra',
              markers=True,
              line_dash='tipo de intercambio')
    st.plotly_chart(fig_andorra,use_container_width=True)


    fig1 = px.bar(filtered_data, x = 'nombre', y = 'Valores', color = 'tipo de intercambio',
             title= 'Valor del intercambio por País y Tipo',
             labels= {'Valores' : 'Valor de intercambio', 'nombre' : 'nombre'},
             barmode= 'group')

    st.plotly_chart(fig1,use_container_width= True)

    fig2 = px.scatter(filtered_data, x = 'Valores', y = 'Porcentaje', color = 'nombre',
                 size= 'Porcentaje', hover_name= 'tipo de intercambio',
                 title = 'Relación entre el valor del intercambio y el porcentaje de cambio',
                 size_max= 10)

    st.plotly_chart(fig2,use_container_width= True)




    if __name__ == "__main__":
        intercambio_app()
