import tornado.web
from tornado.web import asynchronous
from tornado import gen
from rec_api.rec.models.recommend import RandomNewsRecommender,BaysianNewsRecommender
from rec_api.rec.models.user import DimensionalUserModel
from rec_api.rec.settings import TREND_DAYS,REC_COUNT,RSS_COUNT,CAT_COUNT,RANDOM_REC_COUNT,BAYSIAN_REC_COUNT
from rec_api.rec.handlers.basic import BaseRequestHandler
from rec_api.rec.models.error import DBError,RECRuntimeError,UserRequestError,HandlerRuntimeError
import cPickle
import traceback

class Rec_Handler(BaseRequestHandler):   
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
                    print "Get in!!!!!!!!!!!!!!!!"
                    res1=RandomNewsRecommender(item_model=self._news_model(),user_model={}).rec(REC_COUNT)
                    
                    print res1[0]
                else:
                    user_id=self.current_user
                    # if not user_id:
                    #     raise UserRequestError(context_info="The user doesn't exist!")
                    cursor=int(self.get_argument('cursor',0))
                    read=self.get_argument('read',[])
                    if read!=[]:
                        read=cPickle.loads(str(read))
                    response=yield gen.Task(self.db.user.find_one,
                            {'_id':float(user_id)},
                            fields={'rss_clickmodel':1,'cat_clickmodel':1})
                    if response[1]['error']:
                        raise DBError(str(user_id),response[1]['error'])
                    elif len(response[0][0])==0:
                        raise UserRequestError(context_info=str(user_id),debug_info="This user doesn't exist")
                    print "response: "
                    print response[0][0]
                    user_model=self._user_model(response[0][0],read)
                    print "user_model: "
                    print user_model['cat_model'].get_model()
                    news_model=self._news_model()
                    res1=BaysianNewsRecommender(user_model,news_model).rec(BAYSIAN_REC_COUNT,cursor)
                    print res1[0]
                    res2=RandomNewsRecommender(news_model,user_model).rec(REC_COUNT-len(res1))
                    res1.extend(res2)
            except DBError as e:
                res1=[]
                self.logger.debug(str(DBError))
            except RECRuntimeError as e:
                res1=[]  
                self.logger.debug(str(RECRuntimeError))        

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
    
    def _user_model(self,res,read):
        trend_model=self._trend_model()
        user_model=DimensionalUserModel()
        res.setdefault('rss_clickmodel',{})
        res.setdefault('cat_clickmodel',{})
        user_model=user_model.init_readlist(read).\
                    init_rssmodel(RSS_COUNT,res['rss_clickmodel'],
                                               trend_model['rss_clickmodel']).\
                    init_catmodel(CAT_COUNT,res['cat_clickmodel'],
                                               trend_model['cat_clickmodel'])
        return user_model

    def _news_model(self):
        """ Return the latest news for Recommendation"""
        self._candidates=self.settings['cached']['candidates']
        return self._candidates.get_data()

    
    def _trend_model(self):
        """Return the click trends of these days"""
        self._trend=self.settings['cached']['trend']        
        return self._trend.get_data()


        

