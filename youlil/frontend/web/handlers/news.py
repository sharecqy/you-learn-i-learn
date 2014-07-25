from web.handlers.base import BaseRequestHandler,authenticated
from web.settings import REC_URL
import tornado.web
from tornado.web import asynchronous
from tornado import gen
from tornado.httpclient import AsyncHTTPClient,HTTPRequest
import cPickle
import urllib
import simplejson as json

class NewsIndexHandler(BaseRequestHandler):
    """
        This handler is to return user's personal page
        which contains some recommended news articles
    """   
    @asynchronous
    @gen.engine    
    def get(self):
        user_id=self.current_user
        cursor=self.get_argument('cursor',0)
        authenticated=self.isAuthenticated()
        read=self.session.get('read',[])
        client=AsyncHTTPClient()
        req_dict={'authenticated':authenticated,'user_id':user_id,'cursor':cursor,'read':cPickle.dumps(read)}
        request=HTTPRequest(url="%s?%s" %(REC_URL,urllib.urlencode(req_dict)),
                            method="GET")
        response=yield gen.Task(client.fetch,request)
        print 'response:  '
        print response
        arts=json.loads(response.body)['rec']
        user={'username':self.session.get('username')}
        context=self.get_context({'arts':arts,'user':user})
        self.write(self.render.newsindex(**context))
        self.finish()

    @asynchronous
    @gen.engine   
    def post(self):
        print self.request.headers
        user_id=self.current_user
        authenticated=self.isAuthenticated()
        if authenticated==0:
            self.write({'redirect':self.get_login_url()})
        else:
            #user_id='13.0'
            cursor=self.get_argument('cursor',0)
            read=self.session.get('read',[])
            client=AsyncHTTPClient()
            req_dict={'authenticated':authenticated,'user_id':user_id,'cursor':cursor,'read':cPickle.dumps(read)}
            request=HTTPRequest(url="%s?%s" %(REC_URL,urllib.urlencode(req_dict)),
                                method="GET")
            response=yield gen.Task(client.fetch,request)
            #arts=json.loads(response.body)['rec']
            self.write({'rec':json.loads(response.body)['rec']})
        self.finish()
        
class NewsHandler(BaseRequestHandler):
    """
        This handler is to return a news article's full text to user
    """
    @asynchronous
    @gen.engine    
    def get(self):
        user_id=self.current_user
        art_id=self.get_argument('art')        
        response=yield gen.Task(self.db.news.find_one,
                                    {'art_id':float(art_id)},
                                    fields={'art_id':1,'rss_id':1,'url':1,'title':1,'content':1}
                                )
        self.art=response[0][0]
        self.user={'user_id':user_id,'username':self.session.get('username')}
        if self.request.headers['User-Agent']!="Android":
            context=self.get_context({'art':self.art,'user':self.user})
            self.write(self.render.news(**context))
        else:
            self.write({'art':self.art})
        self.finish()
        
    def post(self):
        pass

    def on_finish(self):
        """
            Record user's recently read news,then we can filter them 
            out in the recommendation
        """
        if self.isAuthenticated:
            read=self.session.get('read',[])
            read.append(self.art['art_id'])
            """  keep the session in a limited size"""
            if len(read)>50:read=read[25:]
            self.session.set('read',read)
            """Put user's log in a queue"""                
            self.queue.put({'type':'click',
                            'user_id':self.user['user_id'],
                            'art_id':self.art['art_id'],
                            'rss_id':self.art['rss_id']
                            })   
    @property
    def queue(self):
        self._queue=self.settings['queue']
        return self._queue

