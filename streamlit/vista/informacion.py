import streamlit as st
import pandas as pd
import os
import cv2




def informacion_app():
    

    ##### Información de ######
    st.markdown("<h2 style='text-align: center; color: skyblue; font-size: 2rem;'>Más detalles sobre los creadores </h2>", unsafe_allow_html=True)
    st.image("../sources/Banner_4.png")

    st.markdown(
        '<p class="big-font">En esta sección, podrás conocer a los miembros del equipo detrás de este proyecto. Cada uno de nosotros ha contribuido con sus habilidades y experiencia para hacer realidad este trabajo, y estamos disponibles para cualquier consulta o colaboración futura. <br><br>'
        'Esperamos que esta sección te haya proporcionado una visión más clara sobre quiénes somos y el trabajo que hemos realizado en este proyecto. Nos apasiona seguir avanzando en el campo de la tecnología y la ciencia de datos, y estamos siempre abiertos a nuevas oportunidades de colaboración. Te invitamos a explorar nuestro código, seguir nuestras actualizaciones y no dudes en contactarnos a través de LinkedIn para conversar sobre nuestras experiencias o ideas futuras.',
        unsafe_allow_html=True)

    ###################### Info creadores #########################
    width, height = 300, 300
    col, columna_diego, columna_luis, columna_joaquin, columna_victorm = st.columns((0.15,1,1,1,1))

    with columna_diego:
        st.header(":blue[Diego Díaz Gómez]")
        #diego = cv2.imread(filename = "../sources/Diego.png")
        #diego = cv2.cvtColor(diego, cv2.COLOR_BGR2RGB)
        #diego = cv2.resize(diego, width=width, height=height)
        #st.image(diego)

        # Links:
        linkedin, github = st.columns((1,1))

        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/diegodiazgomez/")
        github.link_button("Github", "https://github.com/diegodiazgomez")


    #############################################
    #### Luis #####
    with columna_luis:
        st.header(":blue[Luis Miguel Guerrero Albalat]")
        luis = cv2.imread(filename = "../sources/Luis.png")
        luis = cv2.cvtColor(luis, cv2.COLOR_BGR2RGB)
        luis = cv2.resize(luis, (width, height))
        st.image(luis)

        #Links:
        linkedin, github = st.columns((1,1))

        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/luismguerrero/")
        github.link_button("Github", "https://github.com/LouieGGG")

    ###############################
    ### Joaquin ############
    with columna_joaquin:
        st.header(":blue[Joaquín Acosta]")
        #joaquin = cv2.imread(filename = "../sources/Joaquin.png")
        #joaquin = cv2.cvtColor(joaquin, cv2.COLOR_BGR2RGB)
        #joaquin = cv2.resize(joaquin, width=width, height=height)
        #st.image(joaquin)

        #Links:
        linkedin, github = st.columns((1,1))

        #linkedin.link_button("Linkedin", )
        github.link_button("Github", "https://github.com/AcostaJoaquin" )

    #########
    ### Víctor Manuel ###
    with columna_victorm:
        st.header(":blue[Víctor Manuel Harillo Parra]")
        #victorm = cv2.imread(filename = "../sources/Victor.png")
        #victorm = cv2.cvtColor(victorm, cv2.COLOR_BGR2RGB)
        #victorm = cv2.resize(victorm, width=width, height=height)
        #st.image(victorm)

        #Links:
        linkedin, github = st.columns((1,1))

        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/victormanuelharilloparra")
        github.link_button("Github", "https://github.com/HarilloP")






if __name__ == "__informacion_app_":
    informacion_app()