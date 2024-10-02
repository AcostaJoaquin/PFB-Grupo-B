import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz

def get_intercambio_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'intercambio_electrico.csv')
    intercambio_data = pd.read_csv(data_path)

    if 'Fecha actualización' in intercambio_data.columns:
        intercambio_data['datetime'] = pd.to_datetime(intercambio_data['Fecha actualización'], format='%Y-%m-%d %H:%M:%S%z')
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

    timezone = pytz.timezone("Europe/Madrid")

    if selected_time == '7 días':
        fecha_limite = datetime.now(timezone) - timedelta(days=7)
    elif selected_time == '14 días':
        fecha_limite = datetime.now(timezone) - timedelta(days=14)
    elif selected_time == '30 días':
        fecha_limite = datetime.now(timezone) - timedelta(days=30)
    else:
        fecha_limite = datetime.now(timezone) - timedelta(days=5000)

    filtered_intercambio_data = intercambio_data[intercambio_data['datetime'] >= fecha_limite]

    st.dataframe(filtered_intercambio_data)

if __name__ == "__main__":
    selected_time = st.selectbox("Selecciona un periodo de tiempo", ['7 días', '14 días', '30 días', 'Sin filtro'])
    main(selected_time)
