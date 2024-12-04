# Importación de módulos necesarios de Scrapy
from scrapy.item import Field  # Para definir los campos de los items
from scrapy.item import \
    Item  # Para definir items (estructura de los datos que vamos a extraer)
from scrapy.spiders import \
    CrawlSpider  # Clase base para un spider que realiza un rastreo recursivo
from scrapy.spiders import Rule  # Permite definir reglas para seguir enlaces
from scrapy.linkextractors import LinkExtractor  # Extrae enlaces de las páginas
from scrapy.selector import \
    Selector  # Para seleccionar partes del HTML usando XPath o CSS
from scrapy.loader import \
    ItemLoader  # Para cargar y procesar datos de los items de manera eficiente


class Articulo(Item):
    titulo = Field()
    citaciones = Field()
    autores = Field()
    url = Field()


class GoogleScholar(CrawlSpider):
    name = 'googlescholar'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100,
        'DEPTH_LIMIT': 1, # Para definir que solo se vaya a un nivel de profundidad,
        'FEED_EXPORT_ENCODING': 'utf-8'  # Para evitar problemas con codificacion de simbolos
    }
    allowed_domains = ['scholar.google.com']
    start_urls = [
        'https://scholar.google.com/scholar?as_ylo=2023&q=AI&hl=en&as_sdt=0,5']  # URL inicial donde empieza el rastreo

    download_delay = 1  # Retardo de 1 segundos entre cada solicitud para evitar sobrecargar el servidor

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths='//div[@class="gs_ri"]',
                allow=r'\?cites='
            ), follow=True, callback="parse_start_url"
        ),
    )

    def parse_start_url(self, response):
        sel = Selector(response)
        articulos = sel.xpath('//div[@class="gs_ri"]')

        for articulo in articulos:
            item = ItemLoader(Articulo(), articulo)

            titulo = articulo.xpath('.//h3/a/text()').getall()
            titulo = "".join(titulo)
            item.add_value('titulo', titulo)

            url = articulo.xpath('.//h3/a/@href').get()
            item.add_value('url', url)

            autores = articulo.xpath('.//div[@class="gs_a"]//text()').getall()
            autores = ''.join(autores)
            autores = autores.split('-')[0].strip()
            item.add_value('autores', autores)
            citaciones = 0
            try:
                citaciones = articulo.xpath(
                    './/a[contains(@href, "cites")]/text()').get()
                citaciones = citaciones.replace('Cited by', '')
            except:
                pass

            item.add_value('citaciones', citaciones)

            yield item.load_item()
# scrapy runspider googleSchoolar.py -o articulos.csv