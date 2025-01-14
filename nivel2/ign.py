#Nivel 2
# Importamos los módulos necesarios de Scrapy
from scrapy.spiders import CrawlSpider  # usando CrawlSpider
from scrapy.linkextractors import LinkExtractor  # Necesitamos LinkExtractor para extraer enlaces
from scrapy.selector import Selector  # Selector para manejar las respuestas HTML
from scrapy.loader import ItemLoader  # Para cargar los items
from scrapy.item import Item, Field  # Para definir la estructura de los datos
from scrapy.spiders import CrawlSpider, Rule


# Definición de las clases, que representará los datos que queremos extraer

class Articulo(Item):
    titulo = Field()
    contenido = Field()


class Review(Item):
    titulo = Field()
    calificacion = Field()


class Video(Item):
    titulo = Field()
    fecha_de_publicacion = Field()

class IGNCrawler(CrawlSpider):
    name = 'ign'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100,  # Un poco alto
        'FEED_EXPORT_FIELDS': ['titulo', 'calificacion', 'fecha_de_publicacion', 'contenido'],
        'FEED_EXPORT_ENCODING': 'utf-8'  # Para que se muestren bien los caracteres especiales (ej. acentos)
    }

    allowed_domains = ['latam.ign.com']
    start_urls = ['https://latam.ign.com/se/?model=article&q=ps5']

    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True),  # HORIZONTALIDAD POR TIPO => No tiene callback ya que aqui no voy a extraer datos
        Rule(LinkExtractor(
            allow=r'&page=\d+'
        ), follow=True),
        # HORIZONTALIDAD DE PAGINACION EN CADA TIPO => No tiene callback ya que aqui no voy a extraer datos

        # Una regla por cada tipo de contenido donde ire verticalmente
        # Cada una tiene su propia funcion parse que extraera los items dependiendo de la estructura del HTML donde esta cada tipo de item
        Rule(
            LinkExtractor(  # VERTICALIDAD DE REVIEWS
                allow=r'/review/',
                deny=r'utm_source=recirc',
                # Parametro deny para evitar URLs repetidas que en este caso especial de IGN son por los parametros (https://www.udemy.com/instructor/communication/qa/15832180/detail?course=2861742)
            ), follow=True, callback='parse_review'),
        Rule(
            LinkExtractor(  # VERTICALIDAD DE VIDEOS
                allow=r'/video/',
                deny=r'utm_source=recirc',
            ), follow=True, callback='parse_video'),
        Rule(
            LinkExtractor(
                allow=r'/news/',  # VERTICALIDAD DE ARTICULOS
                deny=r'utm_source=recirc',
            ), follow=True, callback='parse_news'),
    )
# DEFINICION DE CADA FUNCION PARSEADORA DE CADA TIPO DE INFORMACION

# REVIEW
def parse_review(self, response):
    item = ItemLoader(Review(), response)
    item.add_xpath('titulo', '//div[@class="article-headline"]//h1/text()')
    item.add_xpath('calificacion', '//span[@class="side-wrapper side-wrapper hexagon-content"]/div/text()')
    yield item.load_item()

# VIDEO
def parse_video(self, response):
    item = ItemLoader(Video(), response)
    item.add_xpath('titulo', '//h1/text()')
    item.add_xpath('fecha_publicacion', '//span[@class="publish-date"]/text()')
    yield item.load_item()

# ARTICULO
def parse_news(self, response):
    item = ItemLoader(Articulo(), response)
    item.add_xpath('titulo', '//h1/text()')
    item.add_xpath('contenido', '//div[@id="id_text"]//*/text()')
    yield item.load_item()

# scrapy runspider ign.py -o ign.json -t json
