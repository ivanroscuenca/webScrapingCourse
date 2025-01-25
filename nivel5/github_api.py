import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Documentacion del API: https://api.github.com/
endpoint = 'https://api.github.com/user/repos'

password_token = open('./oauthtoken.txt').readline().strip()
response = requests.get(
    endpoint,
    headers=headers,
    auth=('ivanros@protonmail.com', password_token)  # TUPLA DE AUTENTICACION POR MEDIO DE BASIC AUTH
)

# RESPUESTA ESTA EN FORMATO JSON
repositorios = response.json()  # puedo utilizar la libreria json como en la clase, para verla mejor
for repositorio in repositorios:
    print(repositorio["name"])
