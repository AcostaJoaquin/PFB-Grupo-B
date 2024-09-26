import streamlit as st

import numpy as np
import pandas as pd
import requests

def main():

    st.title('REData API')
    st.text('Datos del cuadro de mandro de la red eléctrica de España')


    #Barra lateral
    sidebar_opciones = ['Balance', 'Demanda', 'Generación', 'Intercambio']
    selected_option = st.sidebar.selectbox('Seleccione una opción', sidebar_opciones)

    # Llamada a la API

    ### get_balance_data, get_balance_data, get_generacion_data, get_intercambio_data por determinar.
    if selected_option == 'Balance':
        balance_data = get_balance_data()
        st.subheader('Balance de energía eléctrica')
        st.dataframe(balance_data)

    elif selected_option == 'Demanda':
        demand_data = get_demanda_data()
        st.subheader('Demanda corregida')
        st.dataframe(demand_data)

    elif selected_option == 'Generación':
        generation_data = get_generacion_data()
        st.subheader('Generación')
        st.dataframe(generation_data)

    elif selected_option == 'Intercambio':
        exchange_data = get_intercambio_data
    pass

if __name__ == "__main__":
    main()