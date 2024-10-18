import pandas as pd
import numpy as np
import streamlit as st




def inicio_app():
 




    #Titulo
    st.markdown("<h1 style='text-align: center;color: skyblue; font-size: 3em;'>Proyecto cuadro de mando de la red eléctrica de España</h1>", unsafe_allow_html=True)
    
    #st.image("https://zmscable.es/wp-content/uploads/2023/10/cable-transmision-electricidad.jpg")
    
    #Intro

    col_1,col_2 = st.columns((1,0.2))
    
    col_1.markdown(
        '<p class="big-font">Esta plataforma es el resultado de nuestro proyecto final del curso de <span style="font-weight: bold; color: skyblue">Data Science e Inteligencia Artificial</span> de la escuela <span style="font-weight: bold; color: skyblue">HACK A BOSS</span>.<br>  Fue desarrollado por Diego Díaz Gómez, Luis Miguel Guerrero Albalat, Joaquín Acosta y Víctor Manuel Harillo Parra.<br>' 
        'Se trata de una plataforma interactiva que ofrece un análisis detallado sobre el balance, demanda, generación e intercambio de energía.<br><br>'
        'Este proyecto refleja nuestro esfuerzo conjunto en el uso de herramientas tecnológicas avanzadas para facilitar el análisis energético.<br><br>'
        'Entre sus principales funcionalidades, incluye:<br>',
        unsafe_allow_html=True)
    ####--PESTAÑAS
    tabs1, tabs2, tabs3, tabs4 = st.tabs(["📈:blue[Gráficas interactivas] 📉", ":blue[Mapa Interactivo]🗺️", ":blue[Modelo de Machine Learning]🤖 ", ":blue[Informacíon]📖"])
    with tabs1:
        st.header("Gráficas interactivas")
            #Descripción:
        st.markdown( 'Visualizamos los datos de balance de energía, la demanda, la generación y los intercambios de energía.',
                        unsafe_allow_html=True)
        
    with tabs2:
        st.header(" Mapa Interactivo")
        #Descripción:
        st.markdown("Integramos un mapa dinámico que permite explorar geográficamente los datos de intercambio de energía entre las principales fronteras a España.",
                    unsafe_allow_html=True)
        
    with tabs3:
        st.header("Modelo de Machine Learning")
        #Descripción:
        st.markdown(' Hemos implementado un modelo de aprendizaje automático que realiza predicciones sobre el comportamiento futuro del sistema energético.',
                    unsafe_allow_html=True)
        
    with tabs4:
        st.header("Informacíon:")
        #Descripción:
        st.markdown('Proporciona información sobre nuestro equipo, incluyendo enlaces a nuestros perfiles de GitHub y Linkedin para mayor transparencia y contacto.',
                    unsafe_allow_html=True)
        
        
        
  
    
if __name__ == "__inicio_app__":
    inicio_app()