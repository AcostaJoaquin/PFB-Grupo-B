import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

def get_demanda_data(selected_time):
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'demanda_evolucion.csv')

    demanda_data = pd.read_csv(data_path)

    demanda_data['datetime'] = pd.to_datetime(demanda_data['datetime'], format='%d/%m/%Y')

    if selected_time == '7 días':
        fecha_limite = datetime.now() - timedelta(days=5000)
    elif selected_time == '14 días':
        fecha_limite = datetime.now() - timedelta(days=5000)
    elif selected_time == '30 días':
        fecha_limite = datetime.now() - timedelta(days=5000)

    return demanda_data[demanda_data['datetime'] >= fecha_limite]

def main(selected_time):
    st.subheader('Datos de la demanda eléctrica a nivel nacional')
    demanda_data = get_demanda_data(selected_time)

    st.dataframe(demanda_data[['datetime', 'value']])

if __name__ == "__main__":
    main()
