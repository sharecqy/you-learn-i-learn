import time
from pymongo import Connection, DESCENDING
import datetime
import logging.config
import logging    
from hotqueue import HotQueue
from settings import QUEUE,QUEUE_MOVIE,LOGCONFIG
logging.config.fileConfig(LOGCONFIG)
class Model_Updator:
    def __init__(self):
        con = Connection()
        self.db = con.learner
        self.click_logger=logging.getLogger('userClick')
        self.feedback_logger=logging.getLogger('userFeedback')
        self.click_logger.propagate=False
        self.feedback_logger.propagate=False
        self.queue = QUEUE
        self.queue_movie = QUEUE_MOVIE
        self.rss_dict=self.init_cat()
        self.gen_dict=self.init_genres()
        self.today=self.init_a_day()
    
    
    def init_a_day(self):
        """
            initiate a new day for Trend model
        """
        d=datetime.date.today()
        date=d.strftime('%y_%m_%d')
        today=int(time.mktime(d.timetuple()))
        self.db['trend'].insert({'_id':today,'date':date})
        return today
    
    def init_cat(self):
        """
            initiate a category dictionary
            then we can use it to look up categroy name by rss_id
        """
        rss_dict={}
        for rss in self.db['rss'].find({},{'_id':1,'cat_id':1,'cat_en_name':1,'cat_zh_name':1}):
            rss_dict[rss['_id']]=(rss['cat_id'],rss['cat_en_name'],rss['cat_zh_name'])
        return rss_dict

    def init_genres(self):
        """
            initiate a genres dictionary
            then we can use it to look up genres_id by genres string
        """  
        gen_dict={}
        for gen in self.db['genres'].find({},{'gen_id':1,'gen_name':1}):
            gen_dict[gen['gen_name']]=gen['gen_id']
        return gen_dict
    
    def loop(self):
        """
            Get logs from queue and update user model and trend model            
        """
        while True:
            item=self.queue.get()
            item_movie=self.queue_movie.get()
            print item_movie
            if not item and not item_movie:break
            if item:
                if item['type']=='click':
                    #update user model
                    item['cat_id']=self.rss_dict[item['rss_id']][0]
                    del item['type']
                    print item
                    self.update_user_model(**item)
                    #update trend model
                    del item['user_id']
                    del item['art_id']
                    item['today']=self.today
                    self.update_trend_model(**item)
                    
                elif item['type']=='feedback':
                    del item['type']
                    self.update_feedback_model(**item)
            if item_movie:
                if item_movie['type']=='click':
                    #update user model
                    for gen in item_movie['genres_list']:
                        self.update_genres_model(item_movie['user_id'],self.gen_dict[gen])
                  
    
    def update_user_model(self,user_id,cat_id,art_id,rss_id):
        self.db['user'].update({'_id':user_id},
                    {'$inc':{'.'.join(['cat_clickmodel',str(cat_id)]):1,
                             '.'.join(['rss_clickmodel',str(rss_id)]):1}
                     })
        #logging
        self.click_logger.info('%d %s' %(user_id,art_id))
        
    def update_trend_model(self,today,cat_id,rss_id):
        self.db['trend'].update({'_id':today},
                    {'$inc':{'.'.join(['cat_clickmodel',str(cat_id)]):1,
                             '.'.join(['rss_clickmodel',str(rss_id)]):1}
                     })
    
    def update_feedback_model(self,user_id,art_id,i_score,h_score):
        self.feedback_logger.info('%d %s %s %s' %(user_id,art_id,i_score,h_score))
     
    def update_genres_model(self,user_id,gen_id):
        self.db['user'].update({'_id':user_id},{'$inc':{'.'.join(['mov_clickmodel',str(gen_id)]):1}})

if __name__=='__main__':
    mu=Model_Updator()
    mu.loop()
