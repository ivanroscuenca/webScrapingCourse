# Nivel 1
import requests
from lxml import html
encabezados = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = 'https://www.wikipedia.org'

respuesta = requests.get(url, headers=encabezados)

parser = html.fromstring(respuesta.text)
# Funciones lxml
# ingles = parser.get_element_by_id('js-link-box-en')
# xpath
#ingles = parser.xpath('//a[@id="js-link-box-en"]/strong/text()')
# idiomas = parser.xpath('//a[contains(@id,"js-link-box")]//strong/text()')
# for idioma in idiomas:
#     print(idioma)

idiomas = parser.find_class('central-featured-lang')

for idioma in idiomas:
    print(idioma.text_content())
