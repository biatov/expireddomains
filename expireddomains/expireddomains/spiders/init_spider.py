from scrapy import FormRequest
from ..items import GetUrlDelDomItem
from scrapy.spiders import CrawlSpider
import re
from itertools import groupby


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
                text_link = each.xpath('.//a').extract()
                item['title_del_dom'] = list(filter(None, map(
                    lambda i: i if re.search(r'\((\d+,*)+\)', i) and not re.search('Archive', i) else '', text_link)))
                href = each.xpath('.//a/@href').extract()
                url_del_dom = list(
                    filter(None, map(lambda x: x if re.search('expired[a-zA-Z]+(\d{4,6})*/$', x) else '', href)))
                item['url_del_dom'] = [el for el, _ in groupby(url_del_dom)]
        return item
