# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetUrlDelDomItem(scrapy.Item):
    title_href = scrapy.Field()


class GetDomainsItem(scrapy.Item):
    domain = scrapy.Field()
