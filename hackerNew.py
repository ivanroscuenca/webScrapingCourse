import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = 'https://news.ycombinator.com'

respuesta = requests.get(url, headers=headers)
# parser BeautifulSoup
soup = BeautifulSoup(respuesta.text)

lista_noticias = soup.find_all('tr', class_='athing')

for noticia in lista_noticias:
    titulo = noticia.find('span',class_='titleline').text
    print(titulo)

