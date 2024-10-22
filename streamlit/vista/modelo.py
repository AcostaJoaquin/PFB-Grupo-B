import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

import pickle
from tensorflow.keras.models import load_model
import os



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


def modelo():
    
    demanda_data = get_demanda_data()

    st.subheader(body = "Modelo de Machine Learning :robot_face:")

    st.markdown(body = """En este apartado explicaremos las decisiones tomadas para construir nuestro modelo de
                          Machine Learning y veremos las predicciones realizadas por este""")
    
    st.markdown(body = """Vistas las operaciones que componen el flujo principal de actividades de la red eléctrica 
                          española, la que suscita mayor interés a la hora de intentar predecir su evolución es la 
                          demanda, ya que indica cuanta electricidad se consume o se va a consumir en nuestro país.""")
    
    st.markdown(body = """Es por ello que hemos desarrollado una herramienta que ofrece una aproximación a la que
                          será la demanda energética de los próximos días. Dicha herramienta se basa en un modelo
                          de Machine learning (cuyos detalles se especifican más adelante) entrenado con datos
                          extraidos de la API REData, que permite extraer datos en bruto de los movimientos de 
                          la red eléctrica española. [Para ver más en detalle la API.](https://www.ree.es/es/apidatos)""",
                          unsafe_allow_html=True)


    st.markdown(body = """A continuación puedes conocer en mayor profundidad el modelo 
                          o utilizarlo para predecir la evolución de la demanda eléctrica.""")

    tabs1, tabs2 = st.tabs(["📘:blue[Explicación del modelo]", "⚡:blue[Evolución de la demanda eléctrica]"])
    with tabs1:
        st.header("Explicación del modelo")





    with tabs2:
        st.header("Evolución de la demanda eléctrica")


        st.markdown(body = """Aquí se mostrará la predicción de tantos días como se indique a continuación del último día 
                        de actualización de la página, o de sus equivalentes en años anteriores 
                        si se ha seleccionado otro año.""")
        st.markdown(body = """Tarda unos segundo en cargar, y si se cambian los parámetros 
                              hay que volver a esperar unos segundos.""")


        años = [2024, 2023, 2022]
        año = st.selectbox(label = "Elige año para la proyección de datos", options = años)

        días = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        n_días = st.selectbox(label  = "Di cuántos días quieres predecir",
                                options = días) 


        demanda_filtrado = demanda_data[demanda_data['datetime'].dt.year==año]
        demanda_filtrado = demanda_filtrado.drop (['Fecha actualización', 'datetime'],axis = 1)

        script_dir_1 = os.path.dirname(__file__)
        data_path_1 = os.path.join(script_dir_1, '..', '..', 'Notebooks', 'ML', 'modelo_LSTM_msle.keras')
        modelo = load_model(data_path_1)
        
        script_dir_2 = os.path.dirname(__file__)
        data_path_2 = os.path.join(script_dir_2, '..', '..', 'Notebooks', 'ML', 'scaler.pkl')
        with open(data_path_2, 'rb') as file:
            escalador = pickle.load(file)

        X = pd.DataFrame(demanda_filtrado["Energia_consumida"])
        X = escalador.transform(X)

        # "Multiple - Step Predictions"
        # Toma el último valor de una serie y predice el siguiente
        # Usa esa predicción para seguir haciendo predicciones.


        validation_predictions = list()

        last_x = X

        while len(validation_predictions) <= n_días:
            
            # En la primera iteración predice el siguiente valor usando X
            # En las siguientes iteraciones usa el valor predicho anterior para predecir el siguiente
            p = modelo.predict(last_x.reshape(1, -1, 1))[0, 0]
            
            validation_predictions.append(p)
            # Desplaza los elementos en last_x hacia atras, dejando el primer elemento al final
            last_x = np.roll(last_x, -1)
            
            # Cambia el último elemento a la predicción
            last_x[-1] = p

        validation_predictions = pd.DataFrame(validation_predictions)
        validation_predictions = escalador.inverse_transform(validation_predictions)
        validation_predictions = pd.DataFrame(validation_predictions, columns = ["valores"])

        #Graficamos las predicciones    
        fig_pred = px.line(data_frame= validation_predictions,
                y = "valores")
        fig_pred.update_layout(title = 'Predicción de la evolución de la demanda')
        st.plotly_chart(figure_or_data = fig_pred,
                    use_container_width = True)
















if __name__ == "__main__":
    modelo()