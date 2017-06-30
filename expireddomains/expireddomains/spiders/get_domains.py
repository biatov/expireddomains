from scrapy import FormRequest
from scrapy import Request

from ..items import GetDomainsItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import json


class GetUrlDelDomSpider(CrawlSpider):
    name = 'get_domains'

    allowed_domains = ["expireddomains.net"]

    try:
        with open('title_and_href.json') as f:
            urls = json.load(f)[0]['title_href']
    except FileNotFoundError:
            urls = list()

    start_urls = list(map(lambda link: '%s?start=0' % link, urls))
    # start_urls = ['https://member.expireddomains.net/domains/expiredcom201706/?start=0']
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield Request(url, self.parse, dont_filter=True)

    rules = (
        Rule(LinkExtractor(allow=r'\?start=\d+'), callback='parse_numeric_pages', follow=True),
    )

    def start_requests(self):
        requests = []
        for start_url in self.start_urls:
            requests.append(Request(url=start_url, headers={'Referer': 'https://member.expireddomains.net/'}, dont_filter=True))
        return requests

    def parse(self, response):
        yield FormRequest.from_response(response,
                                        formnumber=1,
                                        formdata={'login': 'orion1da', 'password': '80163440456', 'rememberme': '2'},
                                        callback=self.parse_login)

    def parse_login(self, response):
        if b'The supplied login information are unknown.' not in response.body:
            item = GetDomainsItem()
            for each in response.selector.css('table.base1 tbody '):
                domain_old = each.xpath('tr/td[@class="field_domain"]/a/text()').extract()
                domain_list = list(filter(None,
                                          map(lambda el: el if not re.search('[-\d]', el) and len(el) <= 15 else '',
                                              domain_old)))
                without_dot = list(
                    map(lambda dom: '%s%s' % (dom.split('.')[0][0].lower(), dom.split('.')[0][1:]), domain_list))
                item['domain'] = list(
                    map(lambda i: ''.join(list(map(lambda j: ' %s' % j.lower() if j.isupper() else j, i))),
                        without_dot))
            return item
