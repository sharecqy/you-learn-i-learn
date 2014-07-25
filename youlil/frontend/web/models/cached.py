from pymongo import Connection
from web.settings import MONGO_HOST,MONGO_DBNAME,MONGO_TOPICCOLLCTION
from web.settings import G
import tornado.web
import time
from topic import TopicRanking

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


class HotestTopic(CachedData):
    def __init__(self,count=1000):
        self.count=count
    
    def reload(self):
        """ reload the topics periodically """
        db=self._db(MONGO_HOST,MONGO_DBNAME,MONGO_TOPICCOLLCTION)
        res=db.find({},{'title':1,'content':1,'username':1,'comments':1,'tags':1,'statistic':1,'time_index':1}).sort("time_index",-1).limit(self.count)
        self._conn_close()
        tr=TopicRanking(G)
        topics=list(res)
        for topic in topics:
            topic['comments_num']=len(topic['comments'])
        self._data=tr.sort(topics)
    

