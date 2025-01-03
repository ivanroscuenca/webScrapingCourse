#Nivel 2
# Importamos los módulos necesarios de Scrapy
from scrapy.spiders import CrawlSpider  # usando CrawlSpider
from scrapy.linkextractors import LinkExtractor  # Necesitamos LinkExtractor para extraer enlaces
from scrapy.selector import Selector  # Selector para manejar las respuestas HTML
from scrapy.loader import ItemLoader  # Para cargar los items
from scrapy.item import Item, Field  # Para definir la estructura de los datos
from scrapy.spiders import CrawlSpider, Rule

# Definición de la clase Anuncio, que representará los datos que queremos extraer
class Articulo(Item):
    nombre = Field()  # Nombre del anuncio
    precio = Field()  # Precio del anuncio
    descripcion = Field()  # Descripción del anuncio
    lugar = Field()  # Localidad del anuncio

class MercadoLibreCrawler(CrawlSpider):
    name = 'MercadoLibre'  # Nombre del spider para ser usado al ejecutarlo
    allowed_domains = ['listado.mercadolibre.com.ec', 'articulo.mercadolibre.com.ec']
    start_urls = ['https://listado.mercadolibre.com.ec/animales-mascotas/perros']# URL inicial donde empieza el rastreo
    # Configuración personalizada del spider (en este caso, el User-Agent)
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGEACCOUNT': 2 # se para en la paginacion número 2
        #'ROBOTSTXT_OBEY': False,  # Deshabilitar el cumplimiento del archivo robots.txt
    }
    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 1

 # Definición de las reglas para seguir los enlaces
    rules = (
        #paginación , scroll horizontal
        Rule(
            LinkExtractor(
                allow=r'_Desde_',
                # Expresión para coincidir con los enlaces de paginación
            ),
            follow=True,  # Scrapy seguirá estos enlaces automáticamente

        ),
        #detalle de los productos
        Rule(
            LinkExtractor(
                allow=r'/MEC-',
                # Expresión para coincidir con los enlaces de anuncios
            ),
            follow=True,  # Scrapy seguirá estos enlaces automáticamente
            callback="parse_item"  # Método para procesar la página del anuncio
        ),
    )

    def parse_item(self,response):
        item = ItemLoader(Articulo(), response)  # Cargamos un item Anuncio() en el response para cargar los datos

        # Extraemos los datos de la página utilizando XPath
        item.add_xpath('nombre', '//h1[@class="ui-pdp-title"]/text()')  # XPath para el nombre del producto
        item.add_xpath('precio',
                       '//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__fraction"]/text()')  # XPath para el precio
        item.add_xpath('descripcion', '//p[@class="ui-pdp-description__content"]/text()')  # XPath para la descripción
        item.add_xpath('lugar',
                       '//p[@class="ui-pdp-color--GRAY ui-pdp-family--REGULAR ui-pdp-media__text"]/text()')  # XPath para el lugar

        # Cargamos el item con los datos extraídos y lo devolvemos para su procesamiento posterior
        yield item.load_item()  # "yield" devuelve el item para que Scrapy lo procese (guardar, mostrar, etc.)

        # scrapy runspider mercadolibre.py -o mercadoLibre3.csv -t csv
