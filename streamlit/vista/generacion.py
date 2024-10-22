import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

import plotly.express as px

def get_generacion_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'generacion_estructura.csv')
    print(f"Data path: {data_path}")
    return pd.read_csv(data_path)


def generacion_app(selected_time):
     
    st.markdown("<h1 style='text-align: center; color: skyblue; font-size: 2rem;'>Datos de Generación Eléctrica</h1>", unsafe_allow_html=True)
    
    

    generacion_data = get_generacion_data()

    generacion_data['Fecha actualización'] = pd.to_datetime(generacion_data['Fecha actualización'], format='%d/%m/%Y').dt.tz_localize(None)

    today = pd.to_datetime(generacion_data['Fecha actualización'].iloc[-1]).tz_localize('UTC')
    if selected_time == '7 días':
        date_limit = today - timedelta(days=7)
    elif selected_time == '14 días':
        date_limit = today - timedelta(days=14)
    elif selected_time == '30 días':
        date_limit = today - timedelta(days=30)

    date_limit = date_limit.tz_localize(None)

    filtered_data = generacion_data[generacion_data['Fecha actualización'] >= date_limit]


    fig =px.line(data_frame = filtered_data, x = 'Fecha actualización', y = 'Valores', color = 'nombre',
        line_group= 'tipo de energía',
        title= 'Tipo de energía',
        markers = True)

    st.plotly_chart(fig,use_container_width=True)

    fig2 = px.histogram(data_frame= filtered_data,
             x = 'Valores',
             y = 'Porcentaje',
             color = 'tipo de energía',
             title= 'Histograma por su tipo de energía',
             facet_col= 'tipo de energía',
             nbins= 50)

    st.plotly_chart(fig2,use_container_width=True)

    fig3 = px.box(data_frame = filtered_data,
       x = 'Valores',
       y = 'nombre',
       color= 'nombre')
    st.plotly_chart(fig3,use_container_width=True)

    fig4 = px.box(data_frame = filtered_data,
        x = 'Valores',
        y =  'tipo de energía',
        title = 'Box tipo de energía',
        color =  'tipo de energía')

    st.plotly_chart(fig4,use_container_width=True)

    if __name__ == "__main__":
       generacion_app()
