import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = 'https://news.ycombinator.com'

respuesta = requests.get(url, headers=headers)
# parser BeautifulSoup
soup = BeautifulSoup(respuesta.text, 'lxml')

lista_noticias = soup.find_all('tr', class_='athing')

for noticia in lista_noticias:
    titulo = noticia.find('span',class_='titleline').text
    url = noticia.find('span',class_='titleline').find('a').get('href')

    metadata = noticia.find_next_sibling()
    # Puede ser que una noticia no tenga score o no tenga comentarios
    # Por lo que inicializaremos estos valores en 0
    score = 0
    comentarios = 0

    # La manera mas sencilla de obtener esta metadata es yendo al hermano siguiente
    # del titulo de la noticia
    metadata = noticia.find_next_sibling()

    try:
        score_tmp = metadata.find('span', class_='score').text
        score_tmp = score_tmp.replace('points', '').strip()
        score = int(score_tmp)
    except Exception as e:
        print(e)
        print('No se encontro score')

    try:
        # Para obtener el numero de comentarios, voy a obtener todo el subtitulo de la noticia
        subline = metadata.find(attrs={'class': 'subline'}).text
        # Y voy a hacer un manejo de cadenas de texto para obtener solo el numero de comentarios
        info = subline.split('|')
        comentarios_tmp = info[-1]
        comentarios_tmp = comentarios_tmp.replace('comments', '').strip()
        comentarios = int(comentarios_tmp)
    except:
        print('No se encontraron comentarios')

    print(titulo)
    print(url)
    print(score)
    print(comentarios)
    print()
