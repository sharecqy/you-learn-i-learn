from pymongo import Connection
from rec_api.rec.settings import MONGO_HOST,MONGO_DBNAME,MONGO_NEWSCOLLCTION,MONGO_TRENDCOLLCTION,MONGO_COLLECTION_GENRES,MONGO_MOVIECOLLECTION,MONGO_WEEKLYMOVIES,MONGO_VIDEOCOLLECTION
from rec_api.rec.settings import TREND_DAYS
from news import PlainNewsModel
from movies import PlainMoviesModel
from video import PlainVideoModel
import tornado.web
import time
from datetime import date,timedelta

class CachedData(object):
    def __init__(self):
        raise NotImplementedError("cannot instantiate Abstract Base Class")
    
    def _db(self,host,db,col):
        self.conn=Connection(host=host)
        return self.conn[db][col]
    
    def _conn_close(self):
        self.conn.close()

    def reload(self):
        """ reload data for self._data """
        raise NotImplementedError("This method hasn't been implemented")
    
    def get_data(self):
        if not hasattr(self,'_data'):
            self.reload()
        return self._data            
    
    def __repr__(self):
        return "This is a cached data!"


class Candidate(CachedData):
    def __init__(self,count=200):
        self.count=count
    
    def reload(self):
        """ reload the news periodicallMONGO_NEWSCOLLCTIONy """
        db=self._db(MONGO_HOST,MONGO_DBNAME,MONGO_NEWSCOLLCTION)
        res=db.find({},{'art_id':1,'rss_id':1,'title':1,'description':1,'url':1,'hardness':1}).sort('time_index',-1).limit(self.count)        
        self._conn_close()
        self._data=PlainNewsModel(list(res))
    

class Movies(CachedData):
    def __init__(self,count=5758):       
        self.count=count
        db=self._db(MONGO_HOST,MONGO_DBNAME,MONGO_MOVIECOLLECTION)
        res=db.find({},{'_id':0,'id':1,'genres':1,'ratings':1,'title':1,'year':1,'synopsis':1,'posters':1}).sort('year',-1).limit(self.count)
        self._conn_close()
        data=list(res)
        self._data=PlainMoviesModel(data)

class WeeklyMovies(CachedData):
    def __init__(self):
        db=self._db(MONGO_HOST,MONGO_DBNAME,MONGO_WEEKLYMOVIES)
        movie_ids=db.find({},{'_id':0,'movie_id':1})
        self._conn_close()
        id_list=list(movie_ids)
        db=self._db(MONGO_HOST,MONGO_DBNAME,MONGO_MOVIECOLLECTION)
        data=[]
        for id in id_list:
            res=db.find_one({'id':int(id['movie_id'])},{'_id':0,'id':1,'genres':1,'ratings':1,'title':1,'year':1,'synopsis':1,'posters':1})
            data.append(res)
        self._data=PlainMoviesModel(data)   

class Videos(CachedData):
    def __init__(self,count=2980):
        self.count=count
        db=self._db(MONGO_HOST,MONGO_DBNAME,MONGO_VIDEOCOLLECTION)
        res=db.find({},{'_id':1,'up_count':1,'view_count':1,'title':1,'comment_count':1,'thumbnail':1,'tags':1,'link':1,'down_count':1}).limit(self.count)
        self._conn_close()
        data=list(res)
        self._data=PlainVideoModel(data)
               
class Trend(CachedData):
    def __init__(self,days=TREND_DAYS):
        self.days=days
    
    def reload(self):
        """ reload the news periodically"""
        db=self._db(MONGO_HOST,MONGO_DBNAME,MONGO_TRENDCOLLCTION)
        res=db.find({'_id':{'$lte':self.trend_date[0]},'_id':{'$gte':self.trend_date[1]}})        
        self._data=self._combine_trends(list(res)) 
        self._conn_close()
        
    @property
    def trend_date(self):
        if not hasattr(self, '_trend_date'):
            today=int(time.mktime(date.today().timetuple()))
            self._trend_date=(today,today-self.days)
        return self._trend_date        
    
    def _combine_trends(self,trends):
       res={'cat_clickmodel':{},'rss_clickmodel':{}}
       for trend in trends:
           if trend.has_key('cat_clickmodel'):
               for key,value in trend['cat_clickmodel'].items():
                   res['cat_clickmodel'].setdefault(key,0)
                   res['cat_clickmodel'][key]+=value
           if trend.has_key('rss_clickmodel'):
               for key,value in trend['rss_clickmodel'].items():
                   res['rss_clickmodel'].setdefault(key,0)
                   res['rss_clickmodel'][key]+=value
       return res
