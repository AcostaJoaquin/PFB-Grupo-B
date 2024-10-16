import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

import plotly.express as px

def get_generacion_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'generacion_estructura.csv')
    
    generacion_data = pd.read_csv(data_path)

    if 'Fecha actualización' in generacion_data.columns:
        generacion_data['datetime'] = pd.to_datetime(generacion_data['Fecha actualización'], format='%d/%m/%Y')
    else:
        st.error("La columna 'Fecha actualización' no se encontró en el CSV.")
        return pd.DataFrame()

    return generacion_data

def main(selected_time):
    st.title('Datos de Generación Eléctrica')
    generacion_data = get_generacion_data()

    if selected_time == '7 días':
        fecha_limite = datetime.now() - timedelta(days=4444)
    elif selected_time == '14 días':
        fecha_limite = datetime.now() - timedelta(days=4444)
    elif selected_time == '30 días':
        fecha_limite = datetime.now() - timedelta(days=4440)

    filtered_generacion_data = generacion_data[generacion_data['datetime'] >= fecha_limite]

    st.dataframe(filtered_generacion_data)

    fig =px.line(data_frame = generacion_data, x = 'Fecha actualización', y = 'Valores', color = 'nombre',
        line_group= 'tipo de energía',
        title= 'Tipo de energía',
        markers = True)
    
    st.plotly_chart(fig,use_container_width=True)

    fig2 = px.histogram(data_frame= generacion_data,
             x = 'Valores',
             y = 'Porcentaje',
             color = 'tipo de energía',
             title= 'Histograma por su tipo de energía',
             facet_col= 'tipo de energía',
             nbins= 50)
    
    st.plotly_chart(fig2,use_container_width=True)

    fig3 = px.box(data_frame = generacion_data,
       x = 'Valores',
       y = 'nombre',
       color= 'nombre')
    st.plotly_chart(fig3,use_container_width=True)

    fig4 = px.box(data_frame = generacion_data,
        x = 'Valores',
        y =  'tipo de energía',
        title = 'Box tipo de energía',
        color =  'tipo de energía')
    
    st.plotly_chart(fig4,use_container_width=True)

    if __name__ == "__main__":
        selected_time = st.selectbox("Selecciona un periodo de tiempo", ['7 días', '14 días', '30 días', 'Sin filtro'])
        main(selected_time)
