import requests
from lxml import html

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Abrimos una nueva sesion dentro de scrapy
session = requests.Session()

# Vamos a la pagina donde se encuentra el formulario de Login para obtener
# el authenticity_token que vimos que era necesario para poder logearnos
login_form_url = 'https://github.com/login'
login_form_res = session.get(login_form_url, headers=headers)

# Proceso para obtener el authenticity token que necesitare para el /session
# El FORM DATA siempre se llena en el form de login, por lo tanto, el token
# deberia estar alli
parser_login = html.fromstring(login_form_res.content)
token_especial = parser_login.xpath('//input[@name="authenticity_token"]/@value')

# Este es el URL por tres razones:
# 1. Es el primer endpoint que se llama al dar click en el botón de iniciar sesion.
# 2. es un endpoint de tipo POST. Los inicios de sesion y el procesamiento de formularios casi siempre se realiza en un POST.
# 3. El nombre del endpoint (/session) me indica que es lo que hace.
login_url = 'https://github.com/session'

# Datos obtenidos del FormData que se encuentra en la pestaña de Payload. Una nueva pestaña al lado de la pestaña Headers.
# El nombre de estos parametros cambia entre cada pagina web, usualmente solamente tendremos que definir el usuario y el password
# Basicamente armamos la data que envia el formulario a la login_url
login_data = {
    "login": "ivanros@protonmail.com",
    "password": open('./password.txt').readline().strip(),
    "commit": "Sign in",  # se que lo tengo que poner porque al parecer me indica una acción
    "authenticity_token": token_especial  # se que lo tengo que enviar, porque es un TOKEN. Todo TOKEN es importante
    # timestamp y timestamp_secret también los tenemos pero luego de realizar pruebas, comprobamos que no son importantes
}

# Una vez ejecutado el requerimiento POST a la URL de Login con la data necesaria, yo ya estoy logeado
# Y el objeto session me mantiene logueado para los futuros requerimientos
session.post(
    login_url,
    data=login_data,
    headers=headers
)
# Finalmente entro a la pagina donde quiero sacar la info estando autenticado gracias al session
data_url = 'https://github.com/ivanroscuenca?tab=repositories'
respuesta = session.get(
    data_url,
    headers=headers
)

# Utilizo LXML para parsear el arbol HTML
parser = html.fromstring(respuesta.content)
repositorios = parser.xpath('//h3[@class="wb-break-all"]/a/text()')
for repositorio in repositorios:
    print(repositorio)