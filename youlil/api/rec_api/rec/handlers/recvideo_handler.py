'''
Created on June 14, 2013

@author: unclelee
'''
import tornado.web
from tornado.web import asynchronous
from tornado import gen
from rec_api.rec.models.recommend_video import RandomVideoRecommender
from rec_api.rec.handlers.basic import BaseRequestHandler
from rec_api.rec.models.error import DBError,RECRuntimeError,UserRequestError,HandlerRuntimeError
import cPickle
import traceback

class RecVideo_Handler(BaseRequestHandler):   
    """
        This handler is in charge of returning recomendation result based on user id.
    """
    @asynchronous
    @gen.engine
    def get(self):
        """
            In order to keep the variety of recommendation,we combine the resuls from
            BaysianNewsRecommender and RandomNewsRecommender.
            *Attributes:*
                1.user_id
            *Exception:*
                1.Recommendation Runtime Exception.     return random rec   status code 200
                2.DBError.                              return random rec   status code 200
                3.RequestError(user doesn't exist).     return error info   status code 400             
                3.Runtime Exception.                    return error info   status code 500
        """
        print "went in!!!!!!!!!!!!"
        res1=RandomVideoRecommender(self._videos_model()).rec(6)
        final_res={'rec':res1}
        self.write(final_res)
        self.finish()


    def _videos_model(self):
        """ Return the videos for Recommendation"""
        self._videos=self.settings['cached']['videos']
        return self._videos.get_data()