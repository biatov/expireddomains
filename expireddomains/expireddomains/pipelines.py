# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ExpireddomainsPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = str(item['url_del_dom']) + "\n"
        self.file.write(line)
        return item
