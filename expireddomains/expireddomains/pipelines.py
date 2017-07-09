# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from .spiders.get_domains_spider import GetUrlDelDomSpider


class ExpireddomainsPipeline(object):

    def open_spider(self, spider):
        self.region = GetUrlDelDomSpider.start_urls[0].split('/expired')[1].split('/')[0]
        self.date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.file = open('../%s_domains_%s.txt' % (self.region, self.date), 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        try:
            for each in item['domain']:
                line = str(each) + "\n"
                self.file.write(line)
        except KeyError:
            pass
        return item
