import streamlit as st
import pandas as pd
import os
import cv2




def informacion_app():

    col_img, col_tit = st.columns((0.5, 1))
    ##### Información de ######
    col_img.image("../sources/logo.png")
    col_tit.markdown("<h2 style='text-align: center; color: skyblue; font-size: 2rem;'>Más detalles sobre los creadores </h2>", unsafe_allow_html=True)

    st.image("../sources/Banner_4.png")

    st.markdown(
        '<p class="big-font">En esta sección, podrás conocer a los miembros del equipo detrás de este proyecto. Cada uno de nosotros ha contribuido con sus habilidades y experiencia para hacer realidad este trabajo, y estamos disponibles para cualquier consulta o colaboración futura. <br><br>'
        'Esperamos que esta sección te haya proporcionado una visión más clara sobre quiénes somos y el trabajo que hemos realizado en este proyecto. Nos apasiona seguir avanzando en el campo de la tecnología y la ciencia de datos, y estamos siempre abiertos a nuevas oportunidades de colaboración. Te invitamos a explorar nuestro código, seguir nuestras actualizaciones y no dudes en contactarnos a través de LinkedIn para conversar sobre nuestras experiencias o ideas futuras.',
        unsafe_allow_html=True)

    ###################### Info creadores #########################
    width, height = 300, 300
    col, columna_diego, columna_luis, columna_victorm, columna_joaquin = st.columns((0.15,1,1,1,1))

    with columna_diego:
        st.header(":blue[Diego Díaz]")
        diego = cv2.imread(filename = "../sources/Diego.png")
        diego = cv2.cvtColor(diego, cv2.COLOR_BGR2RGB)
        diego = cv2.resize(diego, (width, height))
        st.image(diego)

        # Links:
        linkedin, github = st.columns((1,1))

        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/diegodiazgomez/")
        github.link_button("Github", "https://github.com/diegodiazgomez")


    #############################################
    #### Luis #####
    with columna_luis:
        st.header(":blue[Luis M. Guerrero]")
        luis = cv2.imread(filename = "../sources/Luis.png")
        luis = cv2.cvtColor(luis, cv2.COLOR_BGR2RGB)
        luis = cv2.resize(luis, (width, height))
        st.image(luis)

        #Links:
        linkedin, github = st.columns((1,1))

        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/luismguerrero/")
        github.link_button("Github", "https://github.com/LouieGGG")

#########
    ### Víctor Manuel ###
    with columna_victorm:
        st.header(":blue[Victor M. Harillo]")
        victorm = cv2.imread(filename = "../sources/Victor.png")
        victorm = cv2.cvtColor(victorm, cv2.COLOR_BGR2RGB)
        victorm = cv2.resize(victorm, (width, height))
        st.image(victorm)

        #Links:
        linkedin, github = st.columns((1,1))

        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/victormanuelharilloparra")
        github.link_button("Github", "https://github.com/HarilloP")

    ###############################
    ### Joaquin ############
    with columna_joaquin:
        st.header(":blue[Joaquín Acosta]")
        joaquin = cv2.imread(filename = "../sources/joaquin.png")
        joaquin = cv2.cvtColor(joaquin, cv2.COLOR_BGR2RGB)
        joaquin = cv2.resize(joaquin, (width, height))
        st.image(joaquin)

        #Links:
        linkedin, github = st.columns((1,1))

        #linkedin.link_button("Linkedin", )
        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/joaquinacde?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app")
        github.link_button("Github", "https://github.com/AcostaJoaquin" )








if __name__ == "__informacion_app_":
    informacion_app()