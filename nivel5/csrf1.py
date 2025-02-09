import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6943.52 Safari/537.36",
}
session = requests.Session()

# Obtener el token CSRF
url_token = 'https://www.bolsadesantiago.com/api/Securities/csrfToken'
response = session.get(url_token, headers=headers)
print("CSRF Response:", response.text)

try:
    token = response.json().get('csrf', None)
    if not token:
        raise ValueError("No se obtuvo un token CSRF válido")
except requests.exceptions.JSONDecodeError:
    print("Error: No se pudo obtener un JSON válido en el CSRF Token")
    exit()

headers['X-Csrf-Token'] = token

# Llamamos al API
url_api = 'https://www.bolsadesantiago.com/api/Comunes/getHoraMercado'
response = session.post(url_api, headers=headers)

print("API Response Status:", response.status_code)
print("API Response Text:", response.text)

try:
    dicionario = response.json()
    print(dicionario)
except requests.exceptions.JSONDecodeError:
    print("Error: La respuesta de la API no es un JSON válido")
