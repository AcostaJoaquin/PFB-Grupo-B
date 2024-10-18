import pandas as pd
import numpy as np
import streamlit as st




def inicio_app():

    #Titulo

    st.markdown("<h1 class='center-font; color: blue;'>Proyecto cuadro de mando de la red eléctrica de España</h1>", unsafe_allow_html=True)

    #Intro


    st.markdown("Esta plataforma es la finalizacion del trabajo en equipo llevado a cabo por Diego Díaz Gomez, Luis Miguel Guerrero Albalat, Joaquien Acosta y Victor Manuel Harillo Parra sobre el proyecto final del bootcamp de Data Science e Inteligencia Artificial de la escuela Hack a Boss.",unsafe_allow_html=True)

if __name__ == "__inicio_app__":
    inicio_app()