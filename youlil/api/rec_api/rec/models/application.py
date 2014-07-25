import tornado.web

class Application(tornado.web.Application):
     def __init__(self, handlers=None, candidates=None,trend=None,default_host="", transforms=None,
                 wsgi=False, **settings):
        tornado.web.Application.__init__(self,
                                         handlers=handlers,
                                         default_host=default_host, 
                                         transforms=transforms,
                                         wsgi=wsgi, **settings)
