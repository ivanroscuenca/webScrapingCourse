from bs4 import BeautifulSoup  # Importa la librería BeautifulSoup para analizar HTML
import cloudscraper  # Importa cloudscraper para realizar solicitudes web que evaden protecciones anti-bot

url = 'https://www.zonaprop.com.ar/cocheras-alquiler-capital-federal.html'  # Define la URL que se va a scrapear

scraper = cloudscraper.create_scraper()  # Crea un objeto scraper de cloudscraper para manejar posibles desafíos anti-bot
response = scraper.get(url)  # Realiza una solicitud GET a la URL y guarda la respuesta
print(response) # Imprime el objeto de respuesta. Útil para verificar si la solicitud fue exitosa (código 200)

soup = BeautifulSoup(response.text, features="lxml")  # Crea un objeto BeautifulSoup para parsear el HTML de la respuesta. 'lxml' es un parser específico.

contenedor_de_anuncios = soup.find_all('div', {"data-qa": "posting PROPERTY"})  # Encuentra todos los elementos 'div' que tienen el atributo 'data-qa' con el valor 'posting PROPERTY'. Estos parecen ser los contenedores de cada anuncio.

for div_anuncio in contenedor_de_anuncios:  # Itera sobre cada contenedor de anuncio encontrado
    titulo = div_anuncio.find('h2').text  # Dentro del contenedor del anuncio, encuentra el elemento 'h2' (que contiene el título) y extrae su texto.
    precio = div_anuncio.find(class_='postingPrices-module__price').text  # Dentro del contenedor, encuentra el elemento con la clase 'postingPrices-module__price' (que contiene el precio) y extrae su texto.  El `class_` es necesario porque `class` es una palabra reservada en Python.
    print(titulo)  # Imprime el título del anuncio
    print(precio)  # Imprime el precio del anuncio