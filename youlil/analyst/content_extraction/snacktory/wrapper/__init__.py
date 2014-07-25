'''
Created on 2012-10-21

@author: cqy
'''
import jpype
import chardet
import threading

from encoding import build_Doc
lock = threading.Lock()
StringReader = jpype.JClass('java.io.StringReader')
class ArticleExtractor(object):
    
    def __init__(self,url=None,html=None,timeout=3000,resolve=True):
        if url!=None and html !=None:
            raise Exception('No text or url provided')
        
        try:
            # make it thread-safe
            if threading.activeCount() > 1:
                if jpype.isThreadAttachedToJVM() == False:
                    jpype.attachThreadToJVM()
            lock.acquire()
            
            extractor = jpype.JClass('de/jetwick/snacktory/HtmlFetcher')()
        finally:
            lock.release()
                
        if url:
            self.result=extractor.fetchAndExtract(url, timeout, resolve)
        else:
            if not isinstance(html, unicode):
                self.result=extractor.Extract(unicode(html, chardet.detect(html)['encoding'],errors='ignore'))
            #html_Enc=build_Doc(html)
            #html= StringReader(html)
            #self.result=extractor.Extract(str(html))
            
    def get_Text(self):
        return self.result.getText()
    
    def get_Title(self):
        return self.result.getTitle()    
    
    def get_Image(self):
        return self.result.getImageUrl()
    
    def get_Video(self):
        return self.result.getVideoUrl()
            
        