'''
Created on 2012-12-3

@author: cqy
'''
import tornado.ioloop
import tornado.web
import tornado.httpserver
from rec_api.rec.handlers.rec_handler import *
from rec_api.rec.handlers.recmovie_handler import * 
from rec_api.rec.handlers.recvideo_handler import * 
from rec_api.rec.handlers.recweekly_handler import * 
from rec_api.rec.models.application import Application
from rec_api.rec.models.cached import Candidate,Trend,Movies,WeeklyMovies,Videos
from rec.settings import SETTINGS
import tornado.options
from tornado.options import define, options

urls=[
      (r"/rec",Rec_Handler),
      (r"/rec_mov",RecMovie_Handler),
      (r"/rec_vdo",RecVideo_Handler),
      (r"/rec_weekly",RecWeekly_Handler),
      ]

def init_cached(io_loop=None):
    candidates=Candidate()
    trend=Trend()
    movies=Movies()
    videos=Videos()
    weekly_movies=WeeklyMovies()
    cached={"candidates":candidates,"trend":trend,'movies':movies,'weekly_movies':weekly_movies,'videos':videos}
    task1=tornado.ioloop.PeriodicCallback(candidates.reload, 60000,io_loop)
    task2=tornado.ioloop.PeriodicCallback(trend.reload, 60000,io_loop)
    task1.start() # start ticking,refresh the candidate
    task2.start()
    return cached

def main():    
    io_loop = tornado.ioloop.IOLoop.instance()
    SETTINGS['cached']=init_cached(io_loop)
    app=Application(handlers=urls,**SETTINGS)
    server=tornado.httpserver.HTTPServer(app)
    server.listen(9003)
    io_loop.start()    


if __name__=="__main__":
    main()
