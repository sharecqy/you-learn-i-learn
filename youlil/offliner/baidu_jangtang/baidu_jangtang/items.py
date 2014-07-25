# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BaikeItem(Item):
    # define the fields for your item here like:
    # name = Field()
    _id=Field()
    url=Field()
    raw=Field()
    title=Field()
    article=Field()
    image_local=Field()
    image=Field()


class ZhidaoItem(Item):
    # define the fields for your item here like:
    # name = Field()
    _id=Field()
    url=Field()
    raw=Field()
    title=Field()
    content=Field()
    best_answer=Field()
    answers=Field()
