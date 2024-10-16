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
    balance_data = get_balance_data()

    balance_data['Fecha actualización'] = pd.to_datetime(balance_data['Fecha actualización']).dt.tz_localize(None)

    today = pd.to_datetime('today').tz_localize('UTC')
    if selected_time == '7 días':
        date_limit = today - timedelta(days=7)
    elif selected_time == '14 días':
        date_limit = today - timedelta(days=14)
    elif selected_time == '30 días':
        date_limit = today - timedelta(days=30)

    date_limit = date_limit.tz_localize(None)

    filtered_data = balance_data[balance_data['Fecha actualización'] >= date_limit]

    st.dataframe(filtered_data)


    df_bal = get_balance_data()
    st.dataframe(df_bal)

    colores_personalizados = px.colors.qualitative.Plotly + px.colors.qualitative.Pastel + px.colors.qualitative.Set1
    colores_personalizados = colores_personalizados[:30]

    fig_all = px.line(data_frame = df_bal,
            x = 'Fecha actualización',
            y = 'Valores',
            color = 'nombre',
            color_discrete_sequence = colores_personalizados,
    )
    fig_all.update_layout(title = 'Evolución de energía diaría unificada')
    st.plotly_chart(figure_or_data = fig_all,
                use_container_width = True)



if __name__ == "__main__":
    main()
