import streamlit as st
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import plotly.express as px

import pickle
from tensorflow.keras.models import load_model
from keras.models import Sequential
from keras.layers import Input, Dense, SimpleRNN, Dropout, LSTM
from keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler

import statsmodels
import os
from datetime import datetime, timedelta
from .connection import demanda_datos


def get_demanda_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'demanda_evolucion.csv')
    
    demanda_data = pd.read_csv(data_path)

    if 'Fecha actualización' in demanda_data.columns:
        demanda_data['datetime'] = pd.to_datetime(demanda_data['Fecha actualización'], format='%d/%m/%Y')
    else:
        st.error("La columna 'Fecha actualización' no se encontró en el CSV.")
        return pd.DataFrame()

    return demanda_data


def main():
    
    demanda_data = get_demanda_data()

    st.subheader(body = "Modelo de Machine Learning :robot_face:")

    st.markdown(body = """En este apartado veremos las predicciones realizadas por el modelo 
                          de Machine Learning que hemos entrenado""")
    
    años = [2023, 2024]
    año = st.select_slider(label  = "Elige este año o el anterior para la proyección de datos",
                              options = años,
                              value = 2024) 
    
    días = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    n_días = st.select_slider(label  = "Di cuántos días quieres predecir",
                              options = días,
                              value = 7) 


    demanda_filtrado = demanda_data[demanda_data['datetime'].dt.year==año]
    demanda_filtrado = demanda_filtrado.drop (['Fecha actualización', 'datetime'],axis = 1)

    modelo = load_model("../../Notebooks/ML/modelo_LSTM_msle.keras")
    with open("../../ML/scaler.pkl", 'rb') as file:
        escalador = pickle.load(file)


    demanda_filtrado = escalador.transform(demanda_filtrado)

    # "Multiple - Step Predictions"
    # Toma el último valor de una serie y predice el siguiente
    # Usa esa predicción para seguir haciendo predicciones.


    validation_predictions = list()

    last_x = x_test[0]

    while len(validation_predictions) < n_días:
        
        # En la primera iteración predice el siguiente valor de usando X
        # En las siguientes iteraciones usa el valor predicho anterior para predecir el siguiente
        p = modelo.predict(last_x.reshape(1, -1, 1))[0, 0]
        
        validation_predictions.append(p)
        print(f"Valor: {last_x[-1][0]}\tPredicción: {p}")
        # Desplaza los elementos en last_x hacia atras, dejando el primer elemento al final
        last_x = np.roll(last_x, -1)
        
        # Cambia el último elemento a la predicción
        last_x[-1] = p


    plt.plot(validation_predictions)
    plt.show()

















if __name__ == "__main__":
    main()