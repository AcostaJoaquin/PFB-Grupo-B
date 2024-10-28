import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from .demanda import demanda_app
from datetime import datetime, timedelta
import cv2


selected_time = '30 días'
selected_year = 2024




def inicio_app():

    col_img, col_tit = st.columns((0.5, 1))

    #Titulo
    logo = cv2.imread(filename = "../sources/logo.png")
    logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)
    logo = cv2.resize(logo, (200, 200))
    col_img.image(logo)
    col_tit.markdown("<h1 style='text-align: center; color: skyblue; font-size: 3em;'>Proyecto cuadro de mando de la red eléctrica de España</h1>", unsafe_allow_html=True)

    st.image("../sources/Banner_4.png")

    #Intro

    col_1,col_2 = st.columns((1,0.2))

    col_1.markdown(
        '<p class="big-font">Esta plataforma interactiva que ofrece un análisis detallado sobre el balance, demanda, generación e intercambio de energía.<br><br>'
        'Este es el resultado de nuestro proyecto final del curso de <span style="font-weight: bold; color: skyblue">Data Science e Inteligencia Artificial</span> de la escuela <span style="font-weight: bold; color: skyblue">HACK A BOSS</span>.<br><br> Fue desarrollado por Diego Díaz Gómez, Luis Miguel Guerrero Albalat, Joaquín Acosta y Víctor Manuel Harillo Parra.<br><br>'
        'Este proyecto refleja nuestro esfuerzo conjunto en el uso de herramientas tecnológicas avanzadas para facilitar el análisis energético.<br><br>'
        'Entre sus principales funcionalidades, incluye:<br>',
        unsafe_allow_html=True)
    ####--PESTAÑAS
    tabs1, tabs2, tabs3 = st.tabs(["📈:blue[Gráficas interactivas] 📉", ":blue[Modelo de Machine Learning]🤖 ", ":blue[Informacíon]📖"])
    with tabs1:
        st.header("Gráficas interactivas")
            #Descripción:
        st.markdown( 'Visualizamos los datos de balance de energía, la demanda, la generación y los intercambios de energía.<br><br>'
                    'En el apartado de intercambio integramos un mapa dinámico que permite explorar geográficamente los datos de intercambio de energía entre las principales fronteras a España.<br><br>'
                    'Para una exploración más detallada y personalizada, le invitamos a visitar la sección de gráficas interactivas. Allí podrá filtrar los datos por fecha, tipo de energía, y analizar tendencias, patrones y relaciones entre los diferentes componentes del sistema.<br><br>'
                    'Aquí tienes un adelanto:',
                        unsafe_allow_html=True)

        demanda_app(selected_time,selected_year)

    with tabs2:
        st.header("Modelo de Machine Learning")
        #Descripción:
        st.markdown(' Hemos implementado un modelo de aprendizaje automático que realiza predicciones sobre el comportamiento futuro del sistema energético.',
                    unsafe_allow_html=True)

    with tabs3:
        st.header("Informacíon:")
        #Descripción:
        st.markdown('Proporciona información sobre nuestro equipo, incluyendo enlaces a nuestros perfiles de GitHub y Linkedin para mayor transparencia y contacto.',
                    unsafe_allow_html=True)

if __name__ == "__inicio_app__":
    inicio_app()