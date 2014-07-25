'''
Created on 2012-10-16

@author: cqy
'''
from scrapy.spider import BaseSpider
from scrapy.http import Request
from baidu_jangtang.items import  ZhidaoItem
from scrapy import log
import re
from scrapy.selector import HtmlXPathSelector
import chardet
from pymongo import Connection
from scrapy.http.cookies import CookieJar

class ZhidaoSpider(BaseSpider):
    con = Connection()
    db = con.jiangtang
    baike = db.zhidao
    max_cookies_num=1000
    current_cookie=1

    pipelines=[
    'ZhidaoExtractPipeline',
    'ZhidaoStorePipeline',
    ]

    name="zhidao_spider"    

    allowed_domains = ["zhidao.baidu.com"]

    start_urls = [
        "http://zhidao.baidu.com/",
    ]

    def hascrawled(self,url):
        m = hashlib.md5()
        _id=m.update(url)
        res=ZhidaoSpider.zhidao.find_one({'_id':_id})
        return res!=None

    def parse(self,response):
        hxs = HtmlXPathSelector(response)

        if re.match('.*zhidao.baidu.com/question/[0-9]*.*',response.url):
            zi=ZhidaoItem()
            zi['url']=response.url
            zi['raw']=unicode(response.body, chardet.detect(response.body)['encoding'],errors='ignore')
            yield zi

        for url in hxs.select('//a/@href').extract():
            if not url.startswith('http:'):
                url="http://baike.baidu.com"+url
            if self.hascrawled(url):
                continue
            ZhidaoSpider.current_cookie=ZhidaoSpider.current_cookie+1
            if ZhidaoSpider.current_cookie>ZhidaoSpider.max_cookies_num:
                ZhidaoSpider.current_cookie=1
            yield Request(url, callback=self.parse,meta={'cookiejar': ZhidaoSpider.current_cookie})        
      
