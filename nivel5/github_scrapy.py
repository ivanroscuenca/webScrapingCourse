from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy


class LoginSpider(Spider):
    name = 'GitHubLogin'
    start_urls = ['https://github.com/login']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'login': 'ivanros@protonmail.com', 'password': open('./password.txt').readline().strip()},
            callback=self.after_login
        )

    def after_login(self, response):
        request = scrapy.Request(
            'https://github.com/ivanroscuenca?tab=repositories',
            callback=self.parse_repositorios
        )
        yield request

    def parse_repositorios(self, response):
        sel = Selector(response);
        repositorios = sel.xpath('//h3[@class="wb-break-all"]/a/text()')
        for repositorio in repositorios:
            print(repositorio.get())

process = CrawlerProcess()
process.crawl(LoginSpider)
process.start()


