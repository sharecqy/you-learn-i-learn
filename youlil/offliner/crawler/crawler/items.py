# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class FeedItem(Item):
    rss_id=Field()
    lang=Field()
    title=Field()
    url=Field()
    time_index=Field()
    pub_date=Field()
    ranking=Field()
    tiny_image=Field()
    site_name=Field()
    
class News(Item):
    _id=Field()
    rss_id=Field()
    url=Field()
    news_source=Field()
    title=Field()
    content=Field()
    #tagged_content=Field()
    #plain_content=Field()
    pub_date=Field()
    time_index=Field()
    tiny_image=Field()
    #top_image=Field()
    ranking=Field()
    description=Field()   #temp fields
    site_name=Field()
    hardness=Field()

"""
class FeedItem(Item):
    # define the fields for your item here like:
    # name = Field()
    _id=Field()
    timeindex=Field()
    language=Field()
    title=Field()
    description=Field()
    links=Field()
    titles=Field()
    pubdate=Field()
    itemurl=Field()
    ranking=Field()
    count=Field()
    source=Field()
    more=Field()
    image=Field()
    
    
    
"""
class FeedArticle(Item):
    _id=Field()
    articleurl=Field()
    title_pylxml=Field()
    text_pylxml=Field()
    images_pylxml=Field()
    title_snacktory=Field()
    images_snacktory=Field()
    text_snacktory=Field()
    
    
