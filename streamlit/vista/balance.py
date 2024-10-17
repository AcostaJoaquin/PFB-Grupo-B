import streamlit as st
import pandas as pd

import os

from datetime import timedelta

import plotly.express as px
import plotly.colors as pc

def get_balance_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'balance_electrico.csv')
    print(f"Data path: {data_path}")
    return pd.read_csv(data_path)

def main(selected_time):
    st.title('Balance de energía eléctrica')
    df_bal = get_balance_data()

    df_bal['Fecha actualización'] = pd.to_datetime(df_bal['Fecha actualización']).dt.tz_localize(None)

    today = pd.to_datetime('today').tz_localize('UTC')
    if selected_time == '7 días':
        date_limit = today - timedelta(days=7)
    elif selected_time == '14 días':
        date_limit = today - timedelta(days=14)
    elif selected_time == '30 días':
        date_limit = today - timedelta(days=30)

    date_limit = date_limit.tz_localize(None)

    filtered_data = df_bal[df_bal['Fecha actualización'] >= date_limit]

    colores_personalizados = px.colors.qualitative.Plotly + px.colors.qualitative.Pastel + px.colors.qualitative.Set1
    colores_personalizados = colores_personalizados[:30]

    fig_all = px.line(data_frame = filtered_data,
            x = 'Fecha actualización',
            y = 'Valores',
            color = 'nombre',
            color_discrete_sequence = colores_personalizados)
    fig_all.update_layout(title = 'Evolución de energía diaría unificada')
    st.plotly_chart(figure_or_data = fig_all,
                use_container_width = True)


    fig_reno = px.line(data_frame = filtered_data[filtered_data['tipo de energía'] == 'Renovable'],
        x = 'Fecha actualización',
        y = 'Valores',
        color = 'nombre',
        color_discrete_sequence = colores_personalizados)

    fig_reno.update_layout(title = 'Evolución de energía diaría renovable')
    st.plotly_chart(figure_or_data = fig_reno,
                use_container_width = True)

    fig_no_reno=px.line(data_frame = filtered_data[filtered_data['tipo de energía'] == 'No-Renovable'],
        x = 'Fecha actualización',
        y = 'Valores',
        color = 'nombre',
        color_discrete_sequence = colores_personalizados)

    fig_no_reno.update_layout(title = 'Evolución de energía diaría no renovable')
    st.plotly_chart(figure_or_data = fig_no_reno,
                use_container_width = True)


    fig_dbc = px.line(data_frame = filtered_data[filtered_data['tipo de energía'] == 'Demanda en b.c.'],
        x = 'Fecha actualización',
        y = 'Valores',
        color = 'nombre',
        color_discrete_sequence = colores_personalizados
)

    fig_dbc.update_layout(title = 'Evolución de energía diaría de demanda en barra central')
    st.plotly_chart(figure_or_data = fig_dbc,
                use_container_width = True)


    fig_box2 = px.box(data_frame=filtered_data,
       x = 'Valores',
       y = 'tipo de energía',
       color = 'tipo de energía',
       color_discrete_sequence = colores_personalizados)
    fig_box2.update_layout(title = 'Boxplot con outliers')
    st.plotly_chart(figure_or_data = fig_box2,
                use_container_width = True)







if __name__ == "__main__":
    main()
