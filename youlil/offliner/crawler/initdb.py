#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-11-19

@author: cqy
'''
from pymongo import Connection
import hashlib
con = Connection()
db = con.learner
category = db.category
rss= db.rss
cat_id=0
rss_id=0
def init_catx(line):
    category.insert({'_id':1,'cat_en_name':'World','cat_zh_name':'世界','lang':'en'})
    category.insert({'_id':1,'cat_en_name':'Business','cat_zh_name':'商业','lang':'en'})
    category.insert({'_id':1,'cat_en_name':'Technology','cat_zh_name':'科技','lang':'en'})
    category.insert({'_id':1,'cat_en_name':'Entertainment','cat_zh_name':'娱乐','lang':'en'})
    category.insert({'_id':1,'cat_en_name':'Sports','cat_zh_name':'体育','lang':'en'})
    category.insert({'_id':1,'cat_en_name':'China','cat_zh_name':'中国','lang':'en'})
    category.insert({'_id':1,'cat_en_name':'Military','cat_zh_name':'军事','lang':'en'})
    
    category.insert({'_id':1,'cat_en_name':'World','cat_zh_name':'世界','lang':'zh'})
    category.insert({'_id':1,'cat_en_name':'Business','cat_zh_name':'商业','lang':'zh'})
    category.insert({'_id':1,'cat_en_name':'Technology','cat_zh_name':'科技','lang':'zh'})
    category.insert({'_id':1,'cat_en_name':'Entertainment','cat_zh_name':'娱乐','lang':'zh'})
    category.insert({'_id':1,'cat_en_name':'Sports','cat_zh_name':'体育','lang':'zh'})
    category.insert({'_id':1,'cat_en_name':'China','cat_zh_name':'中国','lang':'zh'})
    category.insert({'_id':1,'cat_en_name':'Military','cat_zh_name':'军事','lang':'zh'})

def init_cat(line):
    global cat_id
    cat_arr=line.split(':')
    cat_dict={'_id':cat_id,'cat_en_name':cat_arr[1],'cat_zh_name':cat_arr[2][:-2],'lang':cat_arr[0]}
    category.insert(cat_dict)
    print cat_dict
    cat_id+=1
    
def init_rss(flag,line):
    global rss_id
    cat_arr=flag.split(':')
    rss_arr=line.split('~~')
    md5=hashlib.md5()
    if len(rss_arr)==2 and line.endswith(';\r\n'):
        rss_url=rss_arr[1][:-3]
        md5.update(rss_url)
        rss_dict={'_id':rss_id,'enable':1,'site_name':rss_arr[0],'rss_url':rss_url,'cat_en_name':cat_arr[1],'cat_zh_name':cat_arr[2][:-2],'lang':cat_arr[0]}
        rss_id+=1
        rss.insert(rss_dict)
        print rss_dict    
    else:
        print "error:\t %s",line

def init_db():
    f=open('rss.cfg','r')
    flag=''
    rss_count=0
    cat_count=0
    f.readline()
    for line in f.readlines():
        if line.startswith('zh') or line.startswith('en'):
            print line
            init_cat(line)            
            flag=line   
            cat_count+=1         
        elif line.endswith(';\r\n'):
            if line.startswith('google'):
                init_rss(flag,line)
                rss_count+=1
        else:
            print "processed %d categories, %d rss" %(cat_count,rss_count)
            break
        
    f.close()
"""    
cat_dict={'World':0,'Business':1,'Technology':2,'Entertainment':3,'Sports':4}

from pymongo import Connection
con = Connection()
db = con.learner
for key,value in cat_dict.items():
    res=db.rss.update({'cat_en_name':key},{'$set':{'cat_id':value}},multi=True)
"""
    
if __name__=="__main__":
    init_db()
        
