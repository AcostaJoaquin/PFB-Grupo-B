import requests

from datetime import datetime, timedelta

#Parametros del API - Estos no van bajo la variable 'params' sino en el mismo endpoint.
lang    =  input('¿En español (es) o en inglés (en)?') 
category = input('¿Balance, demanda, generación o intercambio?') 
widget   = input()

#Creación de la fecha de consulta.
restaDia = float(input())
now = datetime.now()

ultima_fecha = (now - timedelta(days = restaDia)).strftime('%Y-%m-%d')
hoy = now.strftime('%Y-%m-%d')

query = f"start_date={ultima_fecha}T00:00&end_date={hoy}T23:59&time_trunc=day"


#Headers para la peticion GET
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Host' : 'apidatos.ree.es'
}

#URL del endpoint con los parametros
endpoint = f"https://apidatos.ree.es/{lang}/datos/{category}/{widget}?{query}"
response = requests.get(url = endpoint, headers = headers)
data = response.json()
