# VER RECURSOS DE LA CLASE PARA INSTALAR SCRAPY
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Pregunta(Item):
   pregunta = Field()
   descripcion = Field()

class stackoverflowSpider(Spider):
    name = 'miprimerSpider'
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    start_urls = ['https://stackoverflow.com/questions']

    def parse(self,response):
        sel = Selector(response)
        preguntas = sel.xpath('//div[@id="questions"]//div[@class="question-summary"]')

        for pregunta in preguntas:
            item = ItemLoader(Pregunta(),pregunta)
            item.add_xpath('pregunta','.//h3/a/text()')
            item.add_xpath('descripcion', './/div/text()')

            yield item.load_item()


