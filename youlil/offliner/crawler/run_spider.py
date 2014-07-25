#!/usr/bin/env python
'''
Created on 2012-11-12

@author: cqy
'''

import commands
from pymongo import Connection

con = Connection()
db = con.learner
news_col= db.news

def run(spider_name):
    cmd="scrapy crawl %s" %spider_name
    commands.getstatusoutput(cmd)
    
def autoincrease_field(name):
    res=db.eval('db.runCommand({"findandmodify":"autoincrease","query":{"_id":"%s"},"update":{"$inc":{"seq":1}}})' %name)
    return res['value']['seq']
    
def add_artid():
    res=news_col.find({'art_id':{'$exists':False}},{'_id':1})
    for news in res:
        art_id=autoincrease_field('art_id')
        news_col.update({'_id':news['_id']},{'$set':{'art_id':art_id}})
        
    
def final_procedure():
    news_col.remove({'content':{'$exists':False}})
    add_artid()
    con.close()


if __name__=='__main__':
    run('feed_spider')
    run('news_spider')
    final_procedure()
