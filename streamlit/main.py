import streamlit as st
from vista.home import inicio_app
from vista.balance import balance_app as balance_page
from vista.demanda import demanda_app as demanda_page
from vista.generacion import generacion_app as generacion_page
from vista.intercambio import intercambio_app as intercambio_page
from vista.modelo import main as modelo_page
from datetime import datetime, timedelta


page_gb_img = """
<style>
[data-testid="stSidebar"] {
background-image: url("https://cdn.prod.website-files.com/5ff3273633e29c2a7c8b6c80/62162087f33cd1ae31e1b121_blog_REE%20(1)%20(1)%20(1)%20(2).png");
background-size: cover;
}

[data-testid="stAppViewBlockContainer"] {
background-color: #111111;
}

[data-testid="stHeader"] {
background-color: #202020;
}

</style>


"""
st.markdown(page_gb_img, unsafe_allow_html=True)

def main():
   

    # Barra lateral para la navegación
    sidebar_opciones = ['Inicio','Balance', 'Demanda', 'Generación', 'Intercambio', 'Modelo']
    selected_option = st.sidebar.selectbox('Dato a consultar', sidebar_opciones)

    # Selección del periodo de tiempo
    tiempo_opciones = ['7 días', '14 días', '30 días']
    selected_time = st.sidebar.selectbox('Periodo de tiempo', tiempo_opciones)

    # Llamar a la función de la página seleccionada y pasar el periodo de tiempo
    if selected_option == 'Inicio':
        inicio_app()
    elif selected_option == 'Balance':
        balance_page(selected_time)
    elif selected_option == 'Demanda':
        demanda_page(selected_time)
    elif selected_option == 'Generación':
        generacion_page(selected_time)
    elif selected_option == 'Intercambio':
        intercambio_page(selected_time)
    elif selected_option == 'Modelo':
        modelo_page()

if __name__ == "__main__":
    main()
