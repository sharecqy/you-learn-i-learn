'''
Created on May 21, 2013

@author: unclelee
'''
import tornado.web
from tornado.web import asynchronous
from tornado import gen
from rec_api.rec.models.recommend_movie import BaysianMoviesRecommender,RandomMoviesRecommender
from rec_api.rec.models.user_movie import BaysianUserModel,DimensionalUserModel
from rec_api.rec.settings import GENRES_COUNT,GENRES_USER_VIRTUALCLICK,BAYSIAN_MOVREC_COUNT
from rec_api.rec.handlers.basic import BaseRequestHandler
from rec_api.rec.models.error import DBError,RECRuntimeError,UserRequestError,HandlerRuntimeError
import cPickle
import traceback

class RecMovie_Handler(BaseRequestHandler):   
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
        try:
            try:
                if not int(self.get_argument('authenticated',1)):
                    res1=RandomMoviesRecommender(self._movies_model()).rec(BAYSIAN_MOVREC_COUNT)
                else:
                    user_id=self.current_user
                    # if not user_id:
                    #     raise UserRequestError(context_info="The user doesn't exist!")
                    cursor=int(self.get_argument('cursor',0))
                    watched=self.get_argument('watched',[])
                    if watched!=[]:
                        watched=cPickle.loads(str(watched))
                    response=yield gen.Task(self.db.user.find_one,
                            {'_id':float(user_id)},
                            fields={'mov_clickmodel':1})
                    print "response: "
                    print response[0][0]
                    if response[1]['error']:
                        raise DBError(str(user_id),response[1]['error'])
                    elif len(response[0][0])==0:
                        raise UserRequestError(context_info=str(user_id),debug_info="This user doesn't exist")
                    user_model=self._user_model(response[0][0],watched)
                    movies_model=self._movies_model()

                    res1=BaysianMoviesRecommender(user_model,movies_model).rec(BAYSIAN_MOVREC_COUNT,cursor)
            except DBError as e:
                res1=[]
                self.logger.debug(str(DBError))
            except RECRuntimeError as e:
                res1=[]  
                self.logger.debug(str(RECRuntimeError))       
#             res2=RandomNewsRecommender(user_model,news_model).rec(REC_COUNT-len(res1))
#             res1.extend(res2)
            final_res={'rec':res1}
            self.write(final_res)
        except UserRequestError as e:
            self.logger.debug(str(e))
            self.send_error(400)
        except RECRuntimeError as e:
            self.logger.debug(str(e))
            self.send_error(500)
        except:
            e=HandlerRuntimeError(context_info=str(user_id),debug_info=traceback.format_exc())
            self.logger.debug(str(e))
            self.send_error(500)
        else:
            self.finish()
    
    def _user_model(self,res,watched):
        """ Return the user's click model """
        user_model=DimensionalUserModel()
        res.setdefault('mov_clickmodel',{})
        user_model=user_model.init_watchedlist(watched).init_genresmodel(GENRES_COUNT,res['mov_clickmodel'])
        return user_model
    
    def _movies_model(self):
        """ Return the movies for Recommendation"""
        self._movies=self.settings['cached']['movies']
        return self._movies.get_data()


        

