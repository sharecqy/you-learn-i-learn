#!/usr/bin/env python
# coding: utf-8

'''
Created on 2012-12-3

@author: cqy
'''
TREND_DAYS=86400*10
REC_COUNT=6
RANDOM_REC_COUNT=2
BAYSIAN_REC_COUNT=4
USER_VIRTUALCLICK=5 
TREND_VIRTUALCLICK=100 
RSS_COUNT=15
CAT_COUNT=5
LOGCONFIG="./config/log.cfg"

MONGO_HOST='127.0.0.1'
MONGO_DBNAME='learner'
MONGO_NEWSCOLLCTION='news'
MONGO_TRENDCOLLCTION='trend'
MONGO_RSSCOLLCTION='rss'
MONGO_VIDEOCOLLECTION='videos'



#initiate application configuration
SETTINGS = dict(
            debug=True,
        )

#initiate  database configuration
import asyncmongo
db=asyncmongo.Client(pool_id='rec_dbpool', host='127.0.0.1', 
                  port=27017, maxcached=5, 
                  maxconnections=10, dbname='learner')
SETTINGS['db']=db


def get_rssinfo():
        """
            initiate a category dictionary
            then we can use it to look up categroy by rss_id
        """    
        rss_dict={}
        from pymongo import Connection
        db=Connection(MONGO_HOST)[MONGO_DBNAME]
        for rss in db[MONGO_RSSCOLLCTION].find({},{'_id':1,'cat_id':1,'cat_en_name':1,'cat_zh_name':1}):
            rss_dict[rss['_id']]=(rss['cat_id'],rss['cat_en_name'],rss['cat_zh_name'])
        return rss_dict    
rss_dict=get_rssinfo()


GENRES_COUNT=22
GENRES_USER_VIRTUALCLICK=1
BAYSIAN_MOVREC_COUNT=6
MONGO_MOVIECOLLECTION='movie'
MONGO_WEEKLYMOVIES='movie_weekly'
MONGO_COLLECTION_GENRES='genres'
def get_genresinfo():
        """
            initiate a genres dictionary
            then we can use it to look up genres_id by genres string
        """    
        gen_dict={}
        from pymongo import Connection
        db=Connection(MONGO_HOST)[MONGO_DBNAME]
        for gen in db[MONGO_COLLECTION_GENRES].find({},{'gen_id':1,'gen_name':1}):
            gen_dict[gen['gen_name']]=gen['gen_id']
        return gen_dict    
gen_dict=get_genresinfo()

# import logging.config
# logging.config.fileConfig(LOGCONFIG)
# logger=logging.getLogger('reclog')
# logger.propagate=False
# SETTINGS['logger']=getLogger
"""
cat_dict={0:('World'),
          1:('Business'),
          2:('Technology'),
          3:('Entertainment'),
          4:('Sports')}"
from pymongo import Connection
con = Connection()
db = con.learner
for key,value in cat_dict.items():
    res=db.rss.update({'cat_en_name':key},{'$set':{'cat_id':value}},multi=True)
"""
