# Importación de módulos necesarios de Scrapy
from scrapy.item import Field  # Para definir los campos de los items
from scrapy.item import Item  # Para definir items (estructura de los datos que vamos a extraer)
from scrapy.spiders import CrawlSpider  # Clase base para un spider que realiza un rastreo recursivo
from scrapy.spiders import Rule  # Permite definir reglas para seguir enlaces
from scrapy.linkextractors import LinkExtractor  # Extrae enlaces de las páginas
from scrapy.selector import Selector  # Para seleccionar partes del HTML usando XPath o CSS
from scrapy.loader import ItemLoader  # Para cargar y procesar datos de los items de manera eficiente

"""Definición de la clase Opinion, que representará los datos que 
queremos extraer que en este caso son 4"""


class Opinion(Item):
    titulo = Field()
    nota = Field()
    contenido = Field()
    autor = Field()


class TripAdvisor(CrawlSpider):
    name = "OpinionesTripAdvisor"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100
    }
    allowed_domains = ['tripadvisor.com']
    start_urls = [
        'https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']  # URL inicial donde empieza el rastreo

    download_delay = 1  # Retardo de 1 segundos entre cada solicitud para evitar sobrecargar el servidor

    rules = (
        # paginacion de Hoteles(h)
        Rule(
            LinkExtractor(
                allow=r'-oa\d+-',
            ), follow=True
        ),
        # Detalle de Hoteles(v)
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                # los lugares que extraigo especificamente con restrict_xpaths las urls de las reviews
                restrict_xpaths=['//div[@data-automation="hotel-card-title"]/a']
            ), follow=True
        ),
        # Paginación Opiniones dentro de cada Hotel(h)
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ), follow=True
        ),
        # Detalle perfil usuario(v)
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="reviews-tab"]']
            ), follow=True, callback='parse_opinion'

        ),

    )

    def parse_opinion(self, response):
        sel = Selector(response)
        opiniones = sel.xpath('//div[@id="content"]/div/div')
        autor = sel.xpath('//h1/span/text()').get()
        for opinion in opiniones:
            item = ItemLoader(Opinion(), sel)
            item.add_value('autor', autor)
            item.add_xpath('titulo', '//div[@class="AzIrY b _a VrCoN"]/text()')
            item.add_xpath('nota',
                           'substring(//div[@class="BWFIX Pd"]//svg[@class="UctUV d H0"]//title/text(), 1, 1)')
            item.add_xpath('contenido', '//q/text()')

            yield item.load_item()

# # EJECUCION EN TERMINAL:
# scrapy runspider tripadvisor2.py -o tripusers2.csv -t csv

