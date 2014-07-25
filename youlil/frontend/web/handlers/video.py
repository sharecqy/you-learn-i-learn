import tornado.web
from tornado.web import asynchronous
from web.settings import REC_VDO_URL
from tornado import gen
from web.handlers.base import BaseRequestHandler,authenticated
from tornado.httpclient import AsyncHTTPClient,HTTPRequest
from bson.son import SON
import urllib
import simplejson as json
import datetime
import time
"""
	
"""



class VideoIndexHandler(BaseRequestHandler):
    """
        This handler is to return user's personal page
        which contains some recommended videos
    """   
    @asynchronous
    @gen.engine    
    def get(self):
        user_id=self.current_user
        cursor=self.get_argument('cursor',0)
        authenticated=self.isAuthenticated()
        watched=self.session.get('watched',[])
        client=AsyncHTTPClient()
        req_dict={'authenticated':authenticated,'user_id':user_id}
        """Request for recommendation"""
        request=HTTPRequest(url="%s?%s" %(REC_VDO_URL,urllib.urlencode(req_dict)),
                            method="GET")
        response=yield gen.Task(client.fetch,request)
        videos=json.loads(response.body)['rec']

        """Return the params to the client"""
        context=self.get_context({'videos':videos})
        self.write(self.render.videoindex(**context))
        self.finish()

    @asynchronous
    @gen.engine   
    def post(self):
        user_id=self.current_user
        cursor=self.get_argument('cursor',0)
        watched=self.session.get('watched',[])
        authenticated=self.isAuthenticated()
        if authenticated==0:
            self.write({'redirect':self.get_login_url()})
        else:
            client=AsyncHTTPClient()
            req_dict={'authenticated':authenticated,'user_id':user_id}
            """Request for recommendation"""
            request=HTTPRequest(url="%s?%s" %(REC_VDO_URL,urllib.urlencode(req_dict)),
                                method="GET")
            response=yield gen.Task(client.fetch,request)
            print "response: "
            print response
            self.write({'rec':json.loads(response.body)['rec']})
        self.finish()