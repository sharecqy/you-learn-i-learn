import html2text
import urllib2 as ul
from readability.readability import Document
from scrapy.exceptions import DropItem
from scrapy.selector import HtmlXPathSelector
from pymongo import Connection
import hashlib
class BaikeExtractPipeline(object):
    """
        This class is in charge of retrieve thumbnail image from Goolge news description
    """
    def notThisPipeline(self,spider):
        return self.__class__.__name__ not in getattr(spider,'pipelines',[])
    
    def process_item(self,item,spider):
        if self.notThisPipeline(spider):
            return item
        hxs = HtmlXPathSelector(text=item["raw"])
        image=hxs.select("//*[contains(@id, 'cardpic0')]//a//img/@src").extract()
        if len(image)==0:
       		image=""
        else:
        	image=image[0]
        	#image_local=image_path+image[0][-20:]
       		#f=open(image_local,'w')
       		#data=ul.urlopen(image).read()
       		#f.write(data)
       	item['image']=image
       	article= Document(item['raw']).summary()
       	item['article']= html2text.html2text(article)
       	title=Document(item['raw']).short_title()
       	title=title.split('_')
       	item['title']=title[0]
        return item


class BaikeStorePipeline(object):
    """
        This class is in charge of retrieve thumbnail image from Goolge news description
    """
    con = Connection()
    db = con.jiangtang
    baike = db.baike
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
        del item_dict['raw']
        BaikeStorePipeline.baike.insert(item_dict)

        return item

class ZhidaoExtractPipeline(object):
    """
        This class is in charge of retrieve thumbnail image from Goolge news description
    """
    def notThisPipeline(self,spider):
        return self.__class__.__name__ not in getattr(spider,'pipelines',[])
    
    def process_item(self,item,spider):
        if self.notThisPipeline(spider):
            return item
        hxs = HtmlXPathSelector(text=item["raw"])
        title=hxs.select("//*[contains(@class, 'ask-title')]/text()")
	if len(title):
        	item['title']=title.extract()[0]
	else:
		raise DropItem()

        content=hxs.select("//*[contains(@class, 'q-content')]")
	if len(content):
        	item['content']=html2text.html2text(content[0].extract())
	else:
		item['content']=''
        best_answer=hxs.select("//*[contains(@class, 'best-text')]")
        if len(best_answer):
            item['best_answer']=html2text.html2text(best_answer[0].extract())
        else:
            item['best_answer']=""
        anss=hxs.select("//*[contains(@class, 'answer-text')]")
        ext_ans=[]
        for ans in anss:
            ext_ans.append(html2text.html2text(ans.extract()))
        item['answers']=ext_ans

        return item

class ZhidaoStorePipeline(object):

    con = Connection()
    db = con.jiangtang
    zhidao = db.zhidao
    """
        This class is in charge of retrieve thumbnail image from Goolge news description
    """
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
        del item_dict['raw']
        ZhidaoStorePipeline.zhidao.insert(item_dict)      
        return item
