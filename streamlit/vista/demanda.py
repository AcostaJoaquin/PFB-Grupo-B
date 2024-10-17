import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

import plotly.express as px

def get_demanda_data(selected_time):
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'demanda_evolucion.csv')

    demanda_data = pd.read_csv(data_path)

    demanda_data['Fecha actualización'] = pd.to_datetime(demanda_data['Fecha actualización'], format='%d/%m/%Y')

    if selected_time == '7 días':
        fecha_limite = datetime.now() - timedelta(days=5000)
    elif selected_time == '14 días':
        fecha_limite = datetime.now() - timedelta(days=5000)
    elif selected_time == '30 días':
        fecha_limite = datetime.now() - timedelta(days=5000)

    return demanda_data[demanda_data['Fecha actualización'] >= fecha_limite]

def main(selected_time):
    st.subheader('Datos de la demanda eléctrica a nivel nacional')
    demanda_data = get_demanda_data(selected_time)

    st.dataframe(demanda_data)

    fig_demanda = px.line(data_frame = demanda_data,
        x = 'Fecha actualización',
        y = 'Energia_consumida',
        title= 'Evolución de demanda energética diaría',
        markers= True
)
    st.plotly_chart(fig_demanda,use_container_width= True)
    
if __name__ == "__main__":
    main()
