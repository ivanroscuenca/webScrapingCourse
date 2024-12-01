"""
===========================================
============= CLASE OBSOLETA ==============
====== AHORA UTILIZA CARGA DINAMICA =======
"""
# Importación de módulos necesarios de Scrapy
from scrapy.item import Field  # Para definir los campos de los items
from scrapy.item import Item  # Para definir items (estructura de los datos que vamos a extraer)
from scrapy.spiders import CrawlSpider  # Clase base para un spider que realiza un rastreo recursivo
from scrapy.spiders import Rule  # Permite definir reglas para seguir enlaces
from scrapy.linkextractors import LinkExtractor  # Extrae enlaces de las páginas
from scrapy.selector import Selector  # Para seleccionar partes del HTML usando XPath o CSS
from scrapy.loader import ItemLoader  # Para cargar y procesar datos de los items de manera eficiente


class Farmacia(Item):
    Nombre = Field()
    Precio = Field()

class CruzVerde(CrawlSpider):
    name = 'farmacias'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100
    }
    allowed_domains = ['cruzverde.cl/']
    start_urls = [
        'https://www.cruzverde.cl/medicamentos']  # URL inicial donde empieza el rastreo

    download_delay = 1  # Retardo de 1 segundos entre cada solicitud para evitar sobrecargar el servidor
    #paginación horizontal, añadimos en LinkExtractor tags y attrs para que busque e button con atributo data-url
    rules = Rule(
        LinkExtractor(
            allow=r'start=',
            tags=('a','button'),
            attrs=('href','data-url')
        ), follow=True , callback='parse_farmacia'
    ),

    def parse_farmacia(self,response):
        sel = Selector(response)
        productos = sel.xpath('//div[@class="col-12 col-lg-4"]')

        for producto in productos:
            item = ItemLoader(Farmacia(), producto)
            item.add_xpath('Nombre',
                           './/div[@class="tile-body px-3 pt-3 pb-0 d-flex flex-column pb-0"]//div[@class="pdp-link"]/a/text()')
            item.add_xpath('Precio', './/span[contains(@class, "value ")]/text()')

            yield item.load_item()


#este código no es válido porque la página ha cambiado a carga dinámica