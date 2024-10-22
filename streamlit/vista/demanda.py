import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

import plotly.express as px

def get_demanda_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'demanda_evolucion.csv')
    print(f"Data path: {data_path}")
    return pd.read_csv(data_path)


def demanda_app(selected_time):
    st.markdown("<h1 style='text-align: center; color: skyblue; font-size: 2rem;'>Datos de la demanda eléctrica a nivel nacional</h1>", unsafe_allow_html=True)
    
    demanda_data = get_demanda_data()

    demanda_data['Fecha actualización'] = pd.to_datetime(demanda_data['Fecha actualización'], format='%d/%m/%Y').dt.tz_localize(None)

    today = pd.to_datetime(demanda_data['Fecha actualización'].iloc[-1]).tz_localize('UTC')
    if selected_time == '7 días':
        fecha_limite = today - timedelta(days=7)
    elif selected_time == '14 días':
        fecha_limite = today - timedelta(days=14)
    elif selected_time == '30 días':
        fecha_limite = today - timedelta(days=30)

    fecha_limite = fecha_limite.tz_localize(None)

    filtered_data = demanda_data[demanda_data['Fecha actualización'] >= fecha_limite]

    fig_demanda = px.line(data_frame = filtered_data,
        x = 'Fecha actualización',
        y = 'Energia_consumida',
        title= 'Evolución de demanda energética diaría',
        markers= True)
    st.plotly_chart(fig_demanda,use_container_width= True)

if __name__ == "__main__":
    demanda_app()
