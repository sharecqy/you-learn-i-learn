'''
Created on 2012-10-16

@author: cqy
'''
from scrapy.spider import BaseSpider
from scrapy.http import Request
import feedparser
import datetime
from crawler.items import FeedItem,News
from hotqueue import HotQueue
import cPickle
import time
from pymongo import Connection
import hashlib
import chardet
from scrapy import log
def truncate(s, length):
    if len(s) >= length:
        return s[:length]
    else:
        return s
    
class FeedSpider(BaseSpider):
    pipelines=[
    'GoogleNewsImagePipeline',
    'StoreNewsIntoDbPipeline',
    'PushUrlIntoQueuePipeline',
    ]
    name="feed_spider"
    

    
    def start_requests(self):
        for rss_item in self.get_urls_from_db():
            yield self.make_requests_from_url(rss_item['rss_url'],rss_item['_id'],rss_item['site_name'])
            
    def get_urls_from_db(self):
        con = Connection()
        db = con.learner
        rss= db.rss
        res=rss.find({'enable':1,'lang':'en'},{'_id':1,'rss_url':1,'site_name':1})
        self.log('Feed_spider has get rss from db',level=log.INFO)
        con.close()
        return res
        
    def make_requests_from_url(self, url,id,site_name):
        return Request(url, meta={'rss_id':id,'site_name':site_name},dont_filter=True)

    def _convert_time(self,sequence_time):
        if sequence_time == None:
            time1 = datetime.datetime.now()
            time2 = int(time.mktime(time1.timetuple()))
        else:
            time1 = datetime.datetime(*sequence_time[:6])
            time2 = int(time.mktime(sequence_time))
        return time1,time2
    
    def parse(self,response):
        feed=feedparser.parse(response.body)
        meta=response.meta
        index=0;
        for entry in feed.entries:
            news=News()
            news['url'] = entry.get('link')
            if news['url']:
                if type(news['url'])!=type(u''): 
                    news['url']=unicode(news['url'], chardet.detect(news['url'])['encoding'],errors='ignore')
            else: continue
            """
            news['rss_title'] = entry.get('title')
            if news['rss_title']:
                if type(news['rss_title'])!=type(u''):
                    news['rss_title']=unicode(news['rss_title'], chardet.detect(news['rss_title'])['encoding'],errors='ignore')
            else: continue
            """
            news['description']=entry.get('description')
            if news['description']:
                if type(news['description'])!=type(u''):
                    news['description']=unicode(news['description'], chardet.detect(news['description'])['encoding'],errors='ignore')
            
            sequence_time = entry.get('published_parsed', None) #entry.get('updated_parsed', None) or 
            news['pub_date'],news['time_index']=self._convert_time(sequence_time)
            #datetime.datetime(*sequence_time[:6])
            news['ranking'] = index
            news['rss_id']=meta['rss_id']
            news['site_name']=meta['site_name']            
            index = index+1
            yield news
            


class NewsSpider(BaseSpider):
    pipelines=[
    'NewsExtractPipeline',
    'UpdateNewsInDbPipeline',
    ]
    name="news_spider"
    
    
    def start_requests(self):
        for url in self.get_urls_from_queue():
            yield self.make_requests_from_url(url)
    
    def get_urls_from_queue(self):
        queue = HotQueue("news_url", host="localhost", port=6379, db=0)
        res=set()
        while True:
            url=queue.get()
            if not url:break
            res.add(url)
        queue.clear()
        self.log('News_spider has %d url to crawl' %len(res),level=log.INFO)
        return res
    
    def parse(self,response):
        news=News()
        news['url']=response.url
        news['content']=response.body
        yield news
