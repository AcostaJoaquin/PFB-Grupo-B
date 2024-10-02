import streamlit as st
import pandas as pd
import os
from datetime import timedelta

def get_balance_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'balance_electrico_7d.csv')
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

if __name__ == "__main__":
    main()
