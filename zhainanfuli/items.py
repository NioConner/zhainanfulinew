# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ZhainanfuliItem(Item):
    # define the fields for your item here like:
    name = Field()
    mov_id = Field()
    type = Field()
    place = Field()
    pic = Field()
    xplay_url = Field()

    pass
