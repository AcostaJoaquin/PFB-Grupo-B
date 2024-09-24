import requests

#Parametros del API - Estos no van bajo la variable 'params' sino en el mismo endpoint.
lang    =  "es"
category = "balance"
widget   = "balance-electrico"
query   = "start_date=2019-01-01T00:00&end_date=2019-01-31T23:59&time_trunc=day"
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
data