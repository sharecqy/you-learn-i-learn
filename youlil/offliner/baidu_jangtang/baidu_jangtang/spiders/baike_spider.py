'''
Created on 2012-10-16

@author: cqy
'''
from scrapy.spider import BaseSpider
from scrapy.http import Request
from baidu_jangtang.items import BaikeItem
from scrapy import log
import re
from scrapy.selector import HtmlXPathSelector
import chardet
from pymongo import Connection
import hashlib
from scrapy.http.cookies import CookieJar

class BaikeSpider(BaseSpider):

    con = Connection()
    db = con.jiangtang
    baike = db.baike
    max_cookies_num=1000
    current_cookie=1

    pipelines=[
    'BaikeExtractPipeline',
    'BaikeStorePipeline',
    ]

    name="baike_spider"    

    allowed_domains = ["baike.baidu.com"]

    start_urls = [
        "http://baike.baidu.com/",
    ]

    def hascrawled(self,url):
        m = hashlib.md5()
        _id=m.update(url)
        res=BaikeSpider.baike.find_one({'_id':_id})
        return res!=None

    def parse(self,response):

        hxs = HtmlXPathSelector(response)

        if re.match('.*baike.baidu.com/view/[0-9]*.*',response.url):
            bi=BaikeItem()
            bi['url']=response.url
            bi['raw']=unicode(response.body, chardet.detect(response.body)['encoding'],errors='ignore')
            yield bi

        for url in hxs.select('//a/@href').extract():
            if not url.startswith('http:'):
                url="http://baike.baidu.com"+url
            if self.hascrawled(url):
                continue
            BaikeSpider.current_cookie=BaikeSpider.current_cookie+1
            if BaikeSpider.current_cookie>BaikeSpider.max_cookies_num:
                BaikeSpider.current_cookie=1
            yield Request(url, callback=self.parse,meta={'cookiejar': BaikeSpider.current_cookie})        
