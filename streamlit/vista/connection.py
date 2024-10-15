import pandas as pd
import numpy as np
import mysql.connector
import configparser

import requests

from datetime import datetime, timedelta
from pprint import pprint


lang = input('¿En español (es) o en ingles (en)?')
restaDia = float(input('¿Cuantos días atrás?:____________'))
input_año = int(input('¿Qué año?:_____________'))


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Host": "apidatos.ree.es"
}

##    ---OBTENCIÓN DE DATOS DE BALANCE---

def balance_datos(lang):

    now = datetime.now()
    ultima_fecha = (now - timedelta(days = restaDia)).replace(year = input_año).strftime('%Y-%m-%d')


    hoy = now.replace(year = input_año).strftime('%Y-%m-%d')

    query = f"start_date={ultima_fecha}T00:00&end_date={hoy}T23:59&time_trunc=day"


    endpoint = f"https://apidatos.ree.es/{lang}/datos/balance/balance-electrico?{query}"
    response = requests.get(url = endpoint, headers = headers)
    data = response.json()



    lista_nombres = list()
    lista_tipos = list()
    lista_valores = list()
    lista_porcentajes = list()
    lista_fechas = list()
    lista_dias = list()
    lista_meses = list()
    lista_años = list()


    for dato in data['included']: 
        for info in dato['attributes']['content']:
            nombre = info['type']

            tipo = info['groupId']


            for i in info['attributes']['values']:
                valor = i['value']

                porcentaje = i['percentage']

                fecha = i['datetime']
                fecha = pd.to_datetime(fecha)
                dia = fecha.strftime('%d')
                mes = fecha.strftime('%m')
                año = fecha.strftime('%Y')

                fecha = fecha.strftime("%d/%m/%Y")
          
                lista_nombres.append(nombre)
                lista_tipos.append(tipo)
                lista_valores.append(valor)
                lista_porcentajes.append(porcentaje)
                lista_fechas.append(fecha)
                lista_dias.append(dia)
                lista_meses.append(mes)
                lista_años.append(año)

    df_balance = pd.DataFrame()
    df_balance['nombre']               = lista_nombres
    df_balance['tipo de energía']      = lista_tipos
    df_balance['Valores']              = lista_valores
    df_balance["Porcentaje"]           = lista_porcentajes
    df_balance["Fecha actualización"]  = lista_fechas

    df_balance.to_csv('balance_electrico.csv')   

    # Cargar el CSV
    df = pd.read_csv('../Obtencion datos/balance_electrico.csv', sep=',', parse_dates=['Fecha actualización'])

    # Crear una columna 'id' usando el índice del DataFrame
    df['id'] = df.index + 1  # Genera un id único basado en el índice

    # Renombrar columnas si es necesario
    df.rename(columns={'tipo de energía': 'tipo_energia'}, inplace=True)
    
    # Leer el archivo de configuración
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Obtener los valores del archivo de configuración
    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='red_electrica'
    )

    # Crear cursor
    cursor = conn.cursor()

    # Insertar o actualizar datos en la tabla usando el id
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO balance (id, nombre, tipo_energia, valores, porcentaje, fecha_actualizacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            nombre = VALUES(nombre),
            tipo_energia = VALUES(tipo_energia),
            valores = VALUES(valores),
            porcentaje = VALUES(porcentaje),
            fecha_actualizacion = VALUES(fecha_actualizacion)
            """, (row['id'], row['nombre'], row['tipo_energia'], row['Valores'], row['Porcentaje'], row['Fecha actualización']))

    # Confirmar los cambios
    conn.commit()

    # Cerrar conexión
    cursor.close()
    conn.close()

    print("Datos insertados o actualizados en la tabla 'balance' con éxito.")


    return df_balance


    #df_balance  = balance_datos(lang)


    ###    ---OBTENCIÓN DE DATOS DE DEMANDA--- 

def demanda_datos(lang):
     
    now = datetime.now()
    ultima_fecha = (now - timedelta(days = restaDia)).replace(year = input_año).strftime('%Y-%m-%d')


    hoy = now.replace(year = input_año).strftime('%Y-%m-%d')

    query = f"start_date={ultima_fecha}T00:00&end_date={hoy}T23:59&time_trunc=day"

    endpoint = f"https://apidatos.ree.es/{lang}/datos/demanda/evolucion?{query}"
    response = requests.get(url = endpoint, headers = headers)
    data = response.json()

    datetime_lista = list()
    value_lista = list()
    percentage_lista = list()



    for value in data['included']:
        for content in value['attributes']['values']:
                
                porcentaje = content['percentage']
                valor = content['value']
                
                fecha = content ['datetime']
                fecha = pd.to_datetime(fecha)
                fecha = fecha.strftime("%d/%m/%Y")

                datetime_lista.append(fecha)
                value_lista.append(valor)
                percentage_lista.append(porcentaje)


    df_demanda = pd.DataFrame()
    df_demanda['Fecha actualización'] = datetime_lista
    df_demanda['Energía_consumida'] = value_lista

    df_demanda.to_csv('Demanda_evolucion.csv')

    # Leer el archivo de configuración
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Obtener los valores del archivo de configuración
    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']

    # Cargar el CSV
    df = pd.read_csv('../Obtencion datos/datos_demanda.csv', sep=',', parse_dates=['datetime'])

    # Renombrar la columna datetime a fecha para que coincida con el nombre de la tabla
    df.rename(columns={'datetime': 'fecha'}, inplace=True)

    # Crear una columna 'id' usando el índice del DataFrame
    df['id'] = df.index + 1  # Genera un id único basado en el índice

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='red_electrica'
    )

    # Crear cursor
    cursor = conn.cursor()

    # Insertar o actualizar datos en la tabla usando el id como clave única
    for index, row in df.iterrows():
        cursor.execute("""
        INSERT INTO demanda (id, fecha, porcentaje, valor)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        fecha = VALUES(fecha),
        porcentaje = VALUES(porcentaje),
        valor = VALUES(valor)
        """, (row['id'], row['fecha'], row['percentage'], row['value']))

    # Confirmar los cambios
    conn.commit()

    # Cerrar conexión
    cursor.close()
    conn.close()

    print("Datos insertados o actualizados en la tabla 'demanda' con éxito.")

    return df_demanda


####  ----OBTENCIÓN DE DATOS DE GENERACIÓN---- 


def generacion_datos(lang):

    now = datetime.now()
    ultima_fecha = (now - timedelta(days = restaDia)).replace(year = input_año).strftime('%Y-%m-%d')
    
    hoy = now.replace(year = input_año).strftime('%Y-%m-%d')
    
    query = f'start_date={ultima_fecha}T00:00&end_date={hoy}T23:59&time_trunc=day'


    endpoint = f"https://apidatos.ree.es/{lang}/datos/generacion/estructura-generacion?{query}"
    response = requests.get(url= endpoint, headers= headers)
    data = response.json()

    lista_nombres = list()
    lista_tipos = list()
    lista_valores = list()
    lista_porcentajes = list()
    lista_fechas = list()
    



    for dato in data['included']:
        nombre = dato['attributes']['title']
        tipo = dato['attributes']['type']


        for i in dato['attributes']['values']:
            valor = i['value']

            porcentaje = i['percentage']

            fecha = i['datetime']
            fecha = pd.to_datetime(fecha)
            

            fecha =  fecha.strftime("%d/%m/%Y")

            lista_nombres.append(nombre)
            lista_tipos.append(tipo)
            lista_valores.append(valor)
            lista_porcentajes.append(porcentaje)
            lista_fechas.append(fecha)
            

    df_generacion = pd.DataFrame()
    df_generacion['nombre']               = lista_nombres
    df_generacion['tipo de energía']      = lista_tipos
    df_generacion['Valores']              = lista_valores
    df_generacion["Porcentaje"]           = lista_porcentajes
    df_generacion["Fecha actualización"]  = lista_fechas
    
    df_generacion.to_csv('generacion_estructura.csv')

    # Leer el archivo de configuración
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Obtener los valores del archivo de configuración
    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']

    # Cargar el CSV
    df = pd.read_csv('../Obtencion datos/generacion_estructura.csv', sep=',', parse_dates=['Fecha actualización'])

    # Renombrar las columnas para que coincidan con la estructura de la tabla
    df.rename(columns={
    'tipo de energía': 'tipo_energia', 
    'Valores': 'valores', 
    'Porcentaje': 'porcentaje', 
    'Fecha actualización': 'fecha_actualizacion'
    }, inplace=True)

    # Crear una columna 'id' usando el índice del DataFrame
    df['id'] = df.index + 1  # Genera un id único basado en el índice

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='red_electrica'
    )

    # Crear cursor
    cursor = conn.cursor()

    # Insertar o actualizar datos en la tabla usando el id como clave única
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO generacion (id, nombre, tipo_energia, valores, porcentaje, fecha_actualizacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            nombre = VALUES(nombre),
            tipo_energia = VALUES(tipo_energia),
            valores = VALUES(valores),
            porcentaje = VALUES(porcentaje),
            fecha_actualizacion = VALUES(fecha_actualizacion)
            """, (row['id'], row['nombre'], row['tipo_energia'], row['valores'], row['porcentaje'], row['fecha_actualizacion']))

    # Confirmar los cambios
    conn.commit()

    # Cerrar conexión
    cursor.close()
    conn.close()

    print("Datos insertados o actualizados en la tabla 'generacion' con éxito.")

    return df_generacion


#  --- OBTENCIÓN DE DATOS DE INTERCAMBIO ---

def intercambio_datos(lang):
    now = datetime.now()
    ultima_fecha = (now - timedelta(days = restaDia)).replace(year = input_año).strftime('%Y-%m-%d')
    hoy = now.replace(year = input_año).strftime('%Y-%m-%d')

    query = f"start_date={ultima_fecha}T00:00&end_date={hoy}T23:59&time_trunc=day"


    endpoint = f"https://apidatos.ree.es/{lang}/datos/intercambios/todas-fronteras-programados?{query}"
    response = requests.get(url = endpoint, headers = headers)
    data = response.json()


    lista_nombres = list()
    lista_tipos = list()
    lista_valores = list()
    lista_porcentajes = list()
    lista_fechas = list()
   


    for dato in data['included']: 
        for info in dato['attributes']['content']:
            tipo = info['type']

            nombre = info['groupId']


            for i in info['attributes']['values']:
                valor = i['value']

                porcentaje = i['percentage']

                fecha = i['datetime']
                fecha = pd.to_datetime(fecha)
                

                fecha =  fecha.strftime("%d/%m/%Y")

                
                lista_nombres.append(nombre)
                lista_tipos.append(tipo)
                lista_valores.append(valor)
                lista_porcentajes.append(porcentaje)
                lista_fechas.append(fecha)
               


    df_intercambio = pd.DataFrame()
    df_intercambio['nombre']               = lista_nombres
    df_intercambio['tipo de intercambio']      = lista_tipos
    df_intercambio['Valores']              = lista_valores
    df_intercambio["Porcentaje"]           = lista_porcentajes
    df_intercambio["Fecha actualización"]  = lista_fechas

    df_intercambio.to_csv('intercambio_electrico.csv')
             
    # Leer el archivo de configuración
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Obtener los valores del archivo de configuración
    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']

    # Cargar el CSV
    df = pd.read_csv('../Obtencion datos/intercambio_electrico.csv', sep=',', parse_dates=['Fecha actualización'])

    # Renombrar las columnas para que coincidan con la estructura de la tabla
    df.rename(columns={
    'tipo de intercambio': 'tipo_intercambio', 
    'Valores': 'valores', 
    'Porcentaje': 'porcentaje', 
    'Fecha actualización': 'fecha_actualizacion'
    }, inplace=True)

    # Crear una columna 'id' usando el índice del DataFrame
    df['id'] = df.index + 1  # Genera un id único basado en el índice

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='red_electrica'
        )

    # Crear cursor
    cursor = conn.cursor()

    # Insertar o actualizar datos en la tabla usando el id como clave única
    for index, row in df.iterrows():
        cursor.execute("""
        INSERT INTO intercambio (id, nombre, tipo_intercambio, valores, porcentaje, fecha_actualizacion)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        nombre = VALUES(nombre),
        tipo_intercambio = VALUES(tipo_intercambio),
        valores = VALUES(valores),
        porcentaje = VALUES(porcentaje),
        fecha_actualizacion = VALUES(fecha_actualizacion)
        """, (row['id'], row['nombre'], row['tipo_intercambio'], row['valores'], row['porcentaje'], row['fecha_actualizacion']))

    # Confirmar los cambios
    conn.commit()

    # Cerrar conexión
    cursor.close()
    conn.close()

    print("Datos insertados o actualizados en la tabla 'intercambio' con éxito.")

    return df_intercambio 
    