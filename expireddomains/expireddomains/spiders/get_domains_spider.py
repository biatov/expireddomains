from time import sleep
from scrapy import Selector
from ..items import GetDomainsItem
from scrapy.spiders import CrawlSpider
from selenium import webdriver
from pyvirtualdisplay import Display


class GetUrlDelDomSpider(CrawlSpider):
    name = 'get_domains'

    allowed_domains = ["member.expireddomains.net"]

    region = input('Enter region: ').strip()

    start_urls = ['https://member.expireddomains.net/domains/expired%s/' % region]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_id("inputLogin").send_keys('biatovs')
        self.driver.find_element_by_id('inputPassword').send_keys('67129321')
        sleep(4)
        self.driver.find_element_by_id('rememberme').click()
        self.driver.find_element_by_xpath('.//div[@class="form-group"]/div[@class="col-sm-12"]/button[@class="btn btn-default"]').submit()
        self.driver.get('%s?start=0&flimit=25&fmaxhost=15&fnumhost=1&fsephost=1&fwhois=22&flimit=200' % self.start_urls[0])
        if b'The supplied login information are unknown.' not in response.body:
            while True:
                try:
                    selenium_response_text = self.driver.page_source
                    new_selector = Selector(text=selenium_response_text)
                    item = GetDomainsItem()
                    for each in new_selector.xpath('.//table[@class="base1"]/tbody'):
                        domain_list = each.xpath('.//tr/td[@class="field_domain"]/a/text()').extract()
                        without_dot = list(map(lambda dom: '%s%s' % (dom.split('.')[0][0].lower(), dom.split('.')[0][1:]), domain_list))
                        item['domain'] = list(map(lambda i: ''.join(list(map(lambda j: ' %s' % j.lower() if j.isupper() else j, i))), without_dot))
                        yield item
                    next_page = self.driver.find_element_by_xpath('.//a[@class="next"]')
                    next_page.click()
                except:
                    break
        self.driver.close()
        self.display.stop()
