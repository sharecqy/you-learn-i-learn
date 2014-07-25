'''
Created on 2012-11-11

@author: cqy
'''
import random
import hashlib
import copy
import web
from pymongo import Connection, DESCENDING

      
""" An Ariticle_Generator is to generate articles to user based on time age.
    These articles can be used as candidate articles of recommendation system """
con = Connection()
db = con.learner
class Article_Generator:    
    news_col=db.news
    # get the latest articles
    # count is the number of latest articles need to return 
    def get_articles_bycount(self,count=5):
        res = self.news_col.find({'_id':1,'title_pylxml':1,'site_name':1,'description':1,'url':1}).sort('timeindex', DESCENDING).limit(count)
        art_list=[]
        for t in res:
            art=Article(t)
            art['id']=self.get_full_text_link(art['_id'])            
            art_list.append(art)
        return art_list
    
    def get_random_articles(self):
        res = self.news_col.find({},{'_id':1,'rss_id':1,'title':1,'description':1,'url':1}).sort('timeindex', DESCENDING).limit(1000)

        art_list=[]
        for t in res:
            if random.random()>0.01:continue
            art=Article(t)
            art['id']=self.get_full_text_link(art['_id'])            
            art_list.append(art)
        return art_list

    def get_full_text_link(self,id):
        return ''.join(["?art=",id])
        
    def get_full_text(self,id):
        res = self.news_col.find_one({'_id':id},{'rss_id':1,'title':1,'tagged_content':1,'plain_content':1})        
        if not res:
            art_dict={'title':"not existed", 'content':"not existed"}
        art_dict={'id':id,'rss_id':res['rss_id'],'title':res['title'], 'content':res['tagged_content']+res['plain_content']}
        return Article(art_dict)
         
    def get_articles_byhour(self,hour=6):
        pass
    
    def generate_id(self,url):
        md5 = hashlib.md5()
        md5.update(url)
        return md5.hexdigest()
    
    def __repr__(self):
        pass
    
""" A Recommender is to recommend articles based on user's interests,
    user's preference of hardness of reading and some property of articles  """
class Recommender:
    ag=Article_Generator()
    
    def __init__(self,func="random_rec"):
        self.retrend_col=db.trendc_func=func
    
    def __call__(self,count,articles):
        return self.rec_func(count,articles)
    
    def __repr__(self):
        return "The Recommender's strategy is %s " %self.rec_func
    
    def basic_rec(self):
        return self.ag.get_articles_bycount(5,"en")
        
    def random_rec(self):
        return self.ag.get_random_articles()
        

""" A user represent a model of a user
    the model includes personal property(age,sex..), reading history,and english level..."""
class User:
    user_col=db.user   
    trend_col=db.trend 
    def __init__(self,param):  
        self._data=copy.deepcopy(param)
      
    def __getitem__(self,key):
        return self._data[key]
    
    def __setitem__(self,key,value):
        self._data[key]=value
    
    def __repr__(self):
        pass 
    
    def update_click_model(self,user_id,rss_id,cat_name):
        user_col.update({'_id':user_id},
                        {'$inc':{'cat_c_model'.cat_name:1,
                                 'rss_c_model'.rss_id:1}
                         })
        
    def update_feedback_model(self,user_id,rss_id,cat_name):
        pass
    
class Trend:
    pass
        
          


""" An article is a unit of news property.
    property includes news content,difficulty level,word volume,category"""
class Article:
    """ title="",link="",description="",content="",hard_level=3,word_volume=0,category="" """
    
    def __init__(self,param={}):  
        self._data=copy.deepcopy(param)
      
    def __getitem__(self,key):
        return self._data[key]
    
    def __setitem__(self,key,value):
        self._data[key]=value
        
    def __repr__(self):
        return "The Article's title:%s url link:%s description:%s\n" \
                %(self._data["title"],self._data["url"],self._data["description"])


                
class word:
    def __init__(self,word_en,word_zh,word_meaning,sentence,article):
        self.word_en=word_en
        self.sentence=sentence
        
    def __repr__(self):
        return "word_en:%s" %(self.word_en)
