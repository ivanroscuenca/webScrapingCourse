#Nivel 1
import requests
from bs4 import BeautifulSoup

encabezados = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = 'https://stackoverflow.com/questions'

respuesta = requests.get(url, headers=encabezados)

# parser BeautifulSoup
soup = BeautifulSoup(respuesta.text)

contenedor_de_preguntas = soup.find(id='questions')# ENCONTRAR UN ELEMENTO POR ID
lista_de_preguntas = contenedor_de_preguntas.find_all('div', class_="s-post-summary") # ENCONTRAR VARIOS ELEMENTOS POR TAG Y POR CLASE
for pregunta in lista_de_preguntas: # ITERAR ELEMENTO POR ELEMENTO
    texto_pregunta = pregunta.find('h3').text  # DENTRO DE CADA ELEMENTO ITERADO ENCONTRAR UN TAG
    descripcion_pregunta = pregunta.find(class_='s-post-summary--content-excerpt').text  # ENCONTRAR POR CLASE
    descripcion_pregunta = descripcion_pregunta.replace('\n', '').replace('\r','').strip() # LIMPIEZA DE TEXTO
    # print(texto_pregunta)
    # print(descripcion_pregunta)
    # print()

    # METODO #2: APROVECHANDO EL PODER COMPLETO DE BEAUTIFUL SOUP
    contenedor_pregunta2 = pregunta.find('h3')
    texto_pregunta2 = contenedor_pregunta2.text
    descripcion_pregunta2 = contenedor_pregunta2.find_next_sibling('div')  # ATRAVESANDO EL ARBOL DE UNA MENERA DIFERENTE
    texto_descripcion_pregunta2 = descripcion_pregunta2.text
    texto_descripcion_pregunta2= texto_descripcion_pregunta2.replace('\n','').replace('\t', '').strip()
    print (texto_pregunta2)
    print (texto_descripcion_pregunta2)
    print ()



