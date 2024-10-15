import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from modules.ml_func import *
import statsmodels
import os
from datetime import datetime, timedelta
from connection.py import demanda_datos


def ml_app():
    
    st.subheader(body = "Modelo de Machine Learning :robot_face:")

    st.markdown(body = """En este apartado veremos las predicciones realizadas por el modelo 
                          de Machine Learning que hemos entrenado""")

    
    años = ["2023", "2024"]
    año = st.select_slider(label  = "Elige este año o el anterior para la proyección de datos",
                              options = años,
                              value = "2024")
    

    input_año = año - 1
    restaDia = 365
    demanda_datos(lang=es)

    demanda_df = pd.read_csv("../../Obtencion datos/demanda_evolucion.csv")

    st.sidebar.markdown("*"*10)
















