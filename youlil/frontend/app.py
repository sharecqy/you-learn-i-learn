'''
Created on 2012-12-3

@author: cqy
'''
import tornado.ioloop
import tornado.web
import tornado.httpserver
from web.settings import SETTINGS
from web.handlers.login import *  
from web.handlers.news import *
from web.handlers.topic import *
from web.handlers.movie import *
from web.handlers.video import *
from web.handlers.user import *
from web.models.cached import *
import tornado.options
from tornado.options import define, options

urls=[
        ('/',TopicIndexHandler),
        ('/login',LoginHandler),
        ('/register',RegisterHandler),
        ('/logout',LogoutHandler),
        ('/myindex', NewsIndexHandler),
        ('/newsindex', NewsIndexHandler),
        ('/news',NewsHandler),
        ('/topic',TopicHandler),
        ('/topic/comment',AddTPCommentHandler),
        ('/topic/tpvote',VoteTopicHandler),
        ('/topic/comvote',VoteCommentHandler),
        ('/addtopic', AddTopicHandler),
        ('/edittopic', EditTopicHandler),
        ('/topicindex',TopicIndexHandler),
        ('/videoindex', VideoIndexHandler),
        ('/movieindex', MovieIndexHandler),
        ('/movie', MovieHandler),
        ('/movie/comment',AddMovieCommentsHandler),
        ('/mypage',UserIndexHandler),
        #('/words',WordsHandler),
        ('/static/(.*)',tornado.web.StaticFileHandler,{'path':'./web/static'}),
        ('/(.*)',tornado.web.StaticFileHandler,{'path':'./web/static/auth'}),
    ]

def init_cached(io_loop=None):
    ht=HotestTopic()
    ht.reload()
    cached={"hottest_topic":ht}
    task1=tornado.ioloop.PeriodicCallback(ht.reload, 600000,io_loop)
    task1.start() # start ticking,refresh the candidate
    return cached

def main():    
    tornado.options.options.logging = "debug"
    io_loop = tornado.ioloop.IOLoop.instance()
    SETTINGS['cached']=init_cached(io_loop)
    app=tornado.web.Application(handlers=urls,**SETTINGS)
    server=tornado.httpserver.HTTPServer(app)
    server.listen(8003)
    io_loop.start()    


if __name__=="__main__":
    main()
