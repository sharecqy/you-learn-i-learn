#!/usr/bin/python
#-*- coding: utf-8 -*-
import urllib
import urllib2
import json
import time
from pymongo import Connection
con = Connection()
db = con.learner
col=db.videos

client_id='4f1a367d7dbb411a'
auth_url="https://openapi.youku.com/v2/oauth2/authorize"
complete_url="https://openapi.youku.com/v2/searches/keyword/complete.json"
search_keyword_url="https://openapi.youku.com/v2/searches/video/by_keyword.json"
search_tag_url=""
show_basic_batch_url="https://openapi.youku.com/v2/videos/show_basic_batch.json"
show_url="https://openapi.youku.com/v2/videos/show.json"
related_url="https://openapi.youku.com/v2/shows/by_related.json"
def http_client(url,params):
	parameters=urllib.urlencode(params)
	res=urllib2.urlopen(''.join([url,'?',parameters]))
	return res

def search_by_keyword(keyword,count=50,page=1):
	search_params={'client_id':client_id,'keyword':keyword,'period':'history','count':count,'page':page}
	res=http_client(search_keyword_url,search_params)
	return json.loads(res.read())

def search_all_by_keyword(keyword,total=None):
	videos=[]
	page_count=50
	res=search_by_keyword(keyword)
	if not total:total=res['total']
	pages=total/page_count
	videos.extend(res['videos'])
	for i in xrange(2,pages+1):
		res=search_by_keyword(keyword,page_count,i)
		videos.extend(res['videos'])
	return videos


def show_video(video_id):
	show_params={'client_id':client_id,'video_id':video_id}
	res=http_client(show_url,show_params)
	return json.loads(res.read())

def show_related_video(video_id):
	show_params={'client_id':client_id,'video_id':video_id}
	res=http_client(related_url,show_params)
	return json.loads(res.read())

def complete_keyword(keyword):
	show_params={'client_id':client_id,'keyword':keyword}
	res=http_client(complete_url,show_params)
	return json.loads(res.read())

seed=['英语演讲','ted演讲集','english speech']

def get_videos_by_keywords():
	videos=set()
	for keyword in seed:
		vs=search_all_by_keyword(keyword,20)
		for v in vs:
			videos.add(v['id'])
	return videos

def store(videos):
	count=0
        sum=0
	for v in videos:
                x=col.find_one({'_id':v})
                if x:
                    print v,"existed"
                    continue
		v_info=show_video(v)
		v_info['_id']=v_info['id']
		del v_info['id']
		col.insert(v_info)
                sum+=1
                print sum
		if count<700:
			count+=1
                else:
			count=0
			time.sleep(5800)
print "waiting"
#time.sleep(5800)
videos=get_videos_by_keywords()
store(videos)

#params={'client_id':'4f1a367d7dbb411a','response_type':'code','redirect_uri':'http://localhost'}
