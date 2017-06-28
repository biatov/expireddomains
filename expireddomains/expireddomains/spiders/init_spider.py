from scrapy import FormRequest
import scrapy
from ..items import GetUrlDelDomItem
from scrapy.spiders import CrawlSpider


class GetUrlDelDomSpider(CrawlSpider):
    name = "get_url_del_dom"

    allowed_domains = ["expireddomains.net"]

    start_urls = [
        'https://expireddomains.net/login/'
    ]

    def parse(self, response):
        yield FormRequest.from_response(response,
                                        formnumber=1,
                                        formdata={'login': 'orion1da', 'password': '80163440456'},
                                        callback=self.parse_login)

    def parse_login(self, response):
        item = GetUrlDelDomItem()
        if b'The supplied login information are unknown.' not in response.body:
            for each in response.selector.css('ul[id*="navlistexpireddomains"]'):
                item['url_del_dom'] = each.xpath('li/a/text()').extract()
                return item
