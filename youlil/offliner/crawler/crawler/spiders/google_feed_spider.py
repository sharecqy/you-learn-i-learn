'''
Created on 2012-10-16

@author: cqy
'''
from scrapy.spider import BaseSpider
import feedparser
import datetime
from crawler.items import FeedItem,FeedArticle
from hotqueue import HotQueue
import cPickle
import time
def truncate(s, length):
    if len(s) >= length:
        return s[:length]
    else:
        return s
    
class FeedSpider(BaseSpider):
    pipelines=[
    'DescriptionPipeline',
    'FeedItemStorePipeline',
    ]
    name="google_feed_spider"
    """
    "http://news.google.com/news?ned=us&topic=h&output=rss",
    "https://news.google.com/news/feeds?pz=1&cf=all&ned=us&hl=en&topic=tc&output=rss",
    
    urls=[
                
            "https://news.google.com/news/feeds?region=cn&pz=1&cf=all&ned=us&hl=zh-CN&topic=w&output=rss",
            "https://news.google.com/news/feeds?pz=1&cf=all&ned=us&hl=en&topic=w&output=rss"
                
        ]
    """
    
    def __init__(self):
        self.start_urls=FeedSpider.urls
    
        
    def parse(self,response):
        feed=feedparser.parse(response.body)
        index=0;
        for entry in feed.entries:
            feeditem=FeedItem()
            feeditem['itemurl'] = entry.get('link', None).encode('utf-8').strip()
            if feeditem['itemurl'] == None: continue
            feeditem['title'] = truncate(entry.get('title', '').encode('utf-8').strip(), 99)
            feeditem['description']=entry.get('description','')#.encode('utf-8').strip()
            sequence_time = entry.get('published_parsed', None) #entry.get('updated_parsed', None) or 
            if sequence_time == None:
                feeditem['pubdate'] = datetime.datetime.now()
                feeditem['timeindex'] = int(time.mktime(feeditem['pubdate'].timetuple()))
            else:
                feeditem['pubdate'] = datetime.datetime(*sequence_time[:6])
                feeditem['timeindex'] = int(time.mktime(sequence_time))#datetime.datetime(*sequence_time[:6])
            feeditem['ranking'] = index
            index = index+1
            feeditem['source'] = response.url.encode('utf-8').strip()
            if feeditem['source']==self.start_urls[0]:
                feeditem['language']='zh'
            else :
                feeditem['language']='en'
            
            #print feeditem
            yield feeditem
            
    def _get_Links(self):
        pass

queue = HotQueue("learner_links", host="localhost", port=6379, db=0)
class ArticleSpider(BaseSpider):
    pipelines=[
    'ArticlePipeline',
    'ArticleStorePipeline',
    ]
    name="article_spider"
    
    def __init__(self):
        print "meme"
        self.start_urls=[]
        temp=set()
        while True:
            itemDict=queue.get()
            if itemDict==None:break
            itemDict=cPickle.loads(itemDict)
            temp=temp | self._get_Links(itemDict)
        self.start_urls=list(temp)
    
    def parse(self,response):
        article=FeedArticle()
        article['articleurl']=response.url
        article['text_pylxml']=response.body
        yield article
    
    def _get_Links(self,itemDict):
        links=set()
        links.add(itemDict['itemurl'])
        links=links | set(itemDict['links'])
        return links
        
