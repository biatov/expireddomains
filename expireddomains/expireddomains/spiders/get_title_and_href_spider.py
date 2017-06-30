from scrapy import FormRequest
from ..items import GetUrlDelDomItem
from scrapy.spiders import CrawlSpider
import re


class GetUrlDelDomSpider(CrawlSpider):
    name = "get_title_and_href"

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
        if b'The supplied login information are unknown.' not in response.body:
            item = GetUrlDelDomItem()
            for each in response.selector.css('ul[id*="navlistexpireddomains"]'):
                text_link = each.xpath('.//a').extract()

                title_del_dom = list(filter(None, map(
                    lambda i: i if re.search(r'\((\d+,*)+\)', i) and not re.search('Archive', i) else '', text_link)))
                list_del_dom = list(map(lambda sp: re.split('(>.+<)', sp), title_del_dom))
                title = list(map(lambda each_title: each_title[1][1:-1].strip(), list_del_dom))

                url_del_dom = list(filter(None, map(lambda x: x if re.search('expired[a-zA-Z]+(\d{4,6})*/', x) else '',
                                                    title_del_dom)))
                href = list(
                    map(lambda el: '%s%s' % (response.url[:-1], el.split('href="')[1].split('"')[0]), url_del_dom))
                # item['title_href'] = list(zip(title, href))
                item['title_href'] = href
            return item
