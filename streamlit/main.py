import streamlit as st
from vista.balance import main as balance_page
from vista.demanda import main as demanda_page
from vista.generacion import main as generacion_page
from vista.intercambio import main as intercambio_page
from vista.modelo import main as modelo_page
from datetime import datetime, timedelta

def main():
    st.title('REData API')
    st.text('Datos del cuadro de mando de la red eléctrica de España')

    # Barra lateral para la navegación
    sidebar_opciones = ['Balance', 'Demanda', 'Generación', 'Intercambio', 'Modelo']
    selected_option = st.sidebar.selectbox('Dato a consultar', sidebar_opciones)

    # Selección del periodo de tiempo
    tiempo_opciones = ['7 días', '14 días', '30 días']
    selected_time = st.sidebar.selectbox('Periodo de tiempo', tiempo_opciones)

    # Llamar a la función de la página seleccionada y pasar el periodo de tiempo
    if selected_option == 'Balance':
        balance_page(selected_time)
    elif selected_option == 'Demanda':
        demanda_page(selected_time)
    elif selected_option == 'Generación':
        generacion_page(selected_time)
    elif selected_option == 'Intercambio':
        intercambio_page(selected_time)
    elif selected_option == 'Modelo':
        modelo_page(selected_time)

if __name__ == "__main__":
    main()
