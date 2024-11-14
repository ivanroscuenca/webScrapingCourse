from bs4 import BeautifulSoup
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


class Noticia(Item):
    titular = Field()
    descripcion = Field()


class ElUniversoSpider(Spider):
    name = 'MiSegundoSpider'
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    start_urls = ['https://www.eluniverso.com/deportes/']

#BeautifulSoup
    def parse(self, response):
        soup = BeautifulSoup(response.body,
                             'lxml')  # Especifica el parser "lxml" para evitar la advertencia.
        contenedor_noticias = soup.find_all(class_="feed | divide-y relative")

        for contenedor in contenedor_noticias:
            noticias = contenedor.find_all(class_='relative', recursive=False)
            for noticia in noticias:
                item = ItemLoader(Noticia(), response)
                titular = noticia.find('h2').text if noticia.find(
                    'h2') else 'N/A'
                descripcion = noticia.find('p').text if noticia.find(
                    'p') else 'N/A'

                item.add_value('titular', titular)
                item.add_value('descripcion', descripcion)

                yield item.load_item()


        # con scrapy
#         sel = Selector(response)
#         noticias = sel.xpath('//div[contains(@class, "content-feed")]/ul/li')
#         for noticia in noticias:
#             item = ItemLoader(Noticia(), noticia)
#             item.add_xpath('titular', './/h2/a/text()')
#             item.add_xpath('descripcion', './/p/text()')
#
#             yield item.load_item()
#
#
# # EJECUCION EN TERMINAL:
#     # scrapy runspider eluniverso.py -o resumen.json -t json
#

