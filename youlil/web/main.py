#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-11-11

@author: cqy
'''


import web
from pymongo import Connection, DESCENDING
from controller import *
import logging.config
from settings import *
from hotqueue import HotQueue
#web.config.debug = False
#web.config.session_parameters['cookie_name'] = 'xiaowuguike'
#web.config.session_parameters['cookie_domain'] = 'beifen.xiaowuguike.com'
urls = (
        '/', 'Index',
        '/login','Login',
        '/register','Register',
        '/article', 'Article',
        '/myindex', 'MyIndex',
        '/feedback','Feedback',
        '/mywords', 'MyWords',
        '/error', 'Error',
        )
app = web.application(urls, globals(), autoreload=True)
logging.config.fileConfig(logconfig)

# tips: to fix the problem that session can't work at Debug mode
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')                                       # the store object
    session = web.session.Session(app, store, initializer={'login': 0,'usermodel':{}})
    web.config._session = session
else:
    session = web.config._session

        
# make session available in sub-apps
def session_hook():
    web.ctx.session = session

def header_hook():
    web.header('Content-type', "text/html; charset=utf-8")
    


con = Connection()
db = con.learner

queue = HotQueue("youlil", host="localhost", port=6379, db=0)

def data_hook():
    web.ctx.db=db
    web.ctx.queue=queue
    
app.add_processor(web.loadhook(session_hook))
app.add_processor(web.loadhook(header_hook))
app.add_processor(web.loadhook(data_hook))

    


if __name__ == "__main__":
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
