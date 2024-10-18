import pandas as pd
import numpy as np
import streamlit as st




def inicio_app():

    st.image('../../source/vector.png')
    st.markdown(
    """
    <style>
      .background-image {
        background-image: url('https://drive.google.com/file/d/1eed4avDOFutJSjMEuUnRBL5amrRccU2I/view?usp=sharing');
        background-repeat: no-repeat;
        background-position: top right;
        background-size: contain; /* Adjust size as needed */
        position: fixed; /* Keep it in place */
        top: 0;
        right: 0;
        width: 200px; /* Adjust width as needed */
        height: 100px; /* Adjust height as needed */
        z-index: -1; /* Ensure it stays behind other content */
      }
    </style>

    <div class="background-image"></div>
    """,
    unsafe_allow_html=True
)


    #Titulo

    st.markdown("<h1 class='center-font; color: blue;'>Proyecto cuadro de mando de la red eléctrica de España</h1>", unsafe_allow_html=True)

    #Intro


    st.markdown("Esta plataforma es la finalizacion del trabajo en equipo llevado a cabo por Diego Díaz Gomez, Luis Miguel Guerrero Albalat, Joaquien Acosta y Victor Manuel Harillo Parra sobre el proyecto final del bootcamp de Data Science e Inteligencia Artificial de la escuela Hack a Boss.",unsafe_allow_html=True)

if __name__ == "__inicio_app__":
    inicio_app()