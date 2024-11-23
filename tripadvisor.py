
from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

class TripAdvisor(CrawlSpider):
    name = 'Hoteles'
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    download_delay = 2

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ), follow=True, callback="parse_hotel"
        ),
    )

    def parse_hotel(self,response):
         sel = Selector()
         item = ItemLoader(Hotel(), sel)
         item.add_xpath('nombre','//h1[@id="HEADING"]/text()')
         item.add_xpath('precio', '//div[@data-automation="finalPrice"]/text()')
         item.add_xpath('descripcion', '//div[@class="fIrGe _T"]/text()')
         item.add_xpath('amenities',
                        '//div[contains(@data-test-target, "amenity_text")]/text()')

         yield item.load_item()



