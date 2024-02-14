import scrapy

from urllib.parse import urlparse
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    start_urls = ['https://peps.python.org/']
    allowed_domains = [urlparse(url).netloc for url in start_urls]

    def parse(self, response):
        table_cell = response.css('section[id^=numerical-index] tbody tr')
        for table_row in table_cell:
            pep_link = table_row.css('a::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': response.css('h1.page-title::text').get().split()[1],
            'name': response.css('h1.page-title::text').get().split(' – ')[1],
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get()
        }
        yield PepParseItem(data)
