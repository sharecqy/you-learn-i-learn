# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from scrapy.selector import HtmlXPathSelector

from pymongo import Connection
from hotqueue import HotQueue
from urlparse import urlparse
#from decruft.decruft import Document
#from boilerpipe.extract import Extractor as BoilerExtractor
from analyst.hardness.hardness_analyser import ArticleHardnessAnalyzer
from analyst.content_extraction.readability.readability import Document 
from settings import ARTICLE_MIN_LENGTH
#from snacktory.wrapper import ArticleExtractor
import hashlib
import cPickle
import time

class GoogleNewsImagePipeline(object):
    """
        This class is in charge of retrieve thumbnail image from Goolge news description
    """
    def notThisPipeline(self,spider):
        return self.__class__.__name__ not in getattr(spider,'pipelines',[])
    
    def process_item(self,item,spider):
        if self.notThisPipeline(spider):
            return item
        if item['description'] and item['site_name'].startswith('google'):
            item['url']=item['url'].split('url=')[1]
            hxs = HtmlXPathSelector(text=item["description"])
            temp=hxs.select('body/table/tr/td')
            res=temp[0].select('font/a/img/@src').extract()
            image=res[0] if len(res) else None
            if image!=None and image[0:2]=="//":image="http:"+image            
            item['tiny_image']=image
        del item['description']
        del item['site_name']
        return item

class StoreNewsIntoDbPipeline():
    """
        This class is in charge of store feed meta information into database.
    """
    con = Connection()
    db = con.learner
    news = db.news
    
    def notThisPipeline(self,spider):
        return self.__class__.__name__ not in getattr(spider,'pipelines',[])
    
    def process_item(self,item,spider):        
        if self.notThisPipeline(spider):
            return item        
        m = hashlib.md5()
        m.update(item['url'])
        _id=m.hexdigest()
        item['_id']=_id
        item_dict=dict(item)
        StoreNewsIntoDbPipeline.news.insert(item_dict)
        return item

class PushUrlIntoQueuePipeline():
    """
        This class is in charge of push url which will be handled by spider into queue. 
    """
    queue = HotQueue("news_url", host="localhost", port=6379, db=0)
    def notThisPipeline(self,spider):
        return self.__class__.__name__ not in getattr(spider,'pipelines',[])
    
    def process_item(self,item,spider):
        if self.notThisPipeline(spider):
            return item        
        PushUrlIntoQueuePipeline.queue.put(item['url'])
        return "success"

class NewsExtractPipeline(object):
    """
        This class is in charge of etract meaningful(title,description,content) data from webpage
    """
    aha=ArticleHardnessAnalyzer()
    def notThisPipeline(self,spider):
        return self.__class__.__name__ not in getattr(spider,'pipelines',[])
    
    def process_item(self,item,spider):
        if self.notThisPipeline(spider):
            return item
    
        html=item['content']
        try:
            item['title'],item['description'],item['content']=self._get_Summary(html,item['url'])
            if len(item['content'])<ARTICLE_MIN_LENGTH:
                raise DropItem("The length of article is less than ARTICLE_MIN_LENGTH")
            item['hardness']=NewsExtractPipeline.aha.article_hardness(text=item['content'])
            #item['top_image'],item['plain_content']=self._get_Content(html)
        except:
            #raise DropItem("Fail to extract content  %s" % item['url'])
            raise
        return item
    
    """  python readability extract meaningful content """
    
    def _get_Summary(self,html,url):
        doc=Document(html,url=url)
        return doc.short_title(),doc.description(),doc.summary()
    
    """ snacktory extract main text"""
    """
    def _get_Content(self,html):
        ae=ArticleExtractor(html=html)
        text=ae.get_Text()
        #title=ae.get_Title()
        image=ae.get_Image()
        
        #print "xx",len(html)
        #extractor=BoilerExtractor(extractor='ArticleExtractor', html=html)
        
        return image,text
    """

class UpdateNewsInDbPipeline(object):
    """
        This class is in charge of updating title,description,content to database.
    """
    con = Connection()
    db = con.learner
    news = db.news
    def notThisPipeline(self,spider):
        return self.__class__.__name__ not in getattr(spider,'pipelines',[])
    
    def process_item(self,item,spider):
        if self.notThisPipeline(spider):
            return item
        m = hashlib.md5()
        m.update(item['url'])
        _id=m.hexdigest()
        item_dict=dict(item)
        UpdateNewsInDbPipeline.news.update({'_id':_id},{'$set':item_dict})
        return "success"
        

