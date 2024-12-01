# Importación de módulos necesarios de Scrapy
from scrapy.item import Item  # Para definir items (estructura de los datos que vamos a extraer)
from scrapy.item import Field  # Para definir los campos de los items
from scrapy.spiders import CrawlSpider  # Clase base para un spider que realiza un rastreo recursivo
from scrapy.spiders import Rule  # Permite definir reglas para seguir enlaces
from scrapy.linkextractors import LinkExtractor  # Extrae enlaces de las páginas
from scrapy.selector import Selector  # Para seleccionar partes del HTML usando XPath o CSS
from scrapy.loader import ItemLoader  # Para cargar y procesar datos de los items de manera eficiente

# Definición de la clase Hotel, que representará los datos que queremos extraer
class Hotel(Item):
    nombre = Field()  # Nombre del hotel
    precio = Field()  # Precio del hotel
    descripcion = Field()  # Descripción del hotel
    amenities = Field()  # Servicios o comodidades del hotel

# Definición de la clase TripAdvisor, que es el spider que rastrea el sitio web
class TripAdvisor(CrawlSpider):
    name = 'Hoteles'  # Nombre del spider para ser usado al ejecutarlo
    # Configuración personalizada del spider (en este caso, el User-Agent)
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']  # URL inicial donde empieza el rastreo

    download_delay = 2  # Retardo de 2 segundos entre cada solicitud para evitar sobrecargar el servidor

    # Definición de las reglas para seguir los enlaces
    rules = (
        Rule(
            LinkExtractor(  # Utilizamos LinkExtractor para extraer enlaces de las páginas
                allow=r'/Hotel_Review-'  # Solo se deben seguir enlaces que contienen '/Hotel_Review-'
            ),
            follow=True,  # Significa que Scrapy seguirá estos enlaces
            callback="parse_hotel"  # Cuando se accede a una página, se llama a este método para procesarla
        ),
    )

    # Método para procesar las páginas de los hoteles
    def parse_hotel(self, response):
        sel = Selector()  # Creamos un selector para manejar el HTML de la respuesta
        item = ItemLoader(Hotel(), sel)  # Cargamos un item (Hotel) en el selector para cargar los datos

        # Extraemos los datos de la página utilizando XPath
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')  # Nombre del hotel
        item.add_xpath('precio', '//div[@data-automation="finalPrice"]/text()')  # Precio del hotel
        item.add_xpath('descripcion', '//div[@class="fIrGe _T"]/text()')  # Descripción del hotel
        item.add_xpath('amenities', '//div[contains(@data-test-target, "amenity_text")]/text()')  # Servicios del hotel

        # Cargamos el item con los datos extraídos y lo devolvemos para su procesamiento posterior
        yield item.load_item()  # "yield" devuelve el item para que Scrapy lo procese (guardar, mostrar, etc.)


# # EJECUCION EN TERMINAL:
# scrapy runspider tripadvisor.py -o resumenTrip.csv -t csv

#actualmente está 403 forbidden, el servidor de TripAdvisor está bloqueando el acceso de Scrapy a la página.