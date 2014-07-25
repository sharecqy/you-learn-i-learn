#!/usr/bin/env python
# coding: utf-8

import random
#from rec_api.rec.models.filter import BlackListFilter
#from rec_api.rec.models.error import RECRuntimeError,GlobalValueError
import traceback
import math
class Recommender: 
    """ 
        A Recommender is to recommend articles based on user's interests,
        user's preference of hardness of reading and some property of articles .
    """  
    def __repr__(self):
        return "The Recommender is %s " %self.__class__.__name__
    
    def _fliter(self,token):
        return True

    @classmethod
    def rec(cls,*args,**kwargs):
        raise NotImplementedError("cannot instantiate Abstract Base Class")
    
    
class RandomMoviesRecommender(Recommender):
    """
        RandomNewsRecommender recommend news randomly.
    """
    def __init__(self,item_model):
        self.item=item_model
        

    def _map_func(self,x):
        return self.item[(x)]

    def rec(self,count):
        """
            RandomNewsRecommender randomly recommend news except ones user has read,
            but in term of speed we introduce a control variable to avoid looping
            too long(it may include some read news finally,it's not important).
            The method ends in (count+control) times loop.
        """
        try:
            res=random.sample(self.item.get_ids(),count)
            print "authen: res: "
            print res
            print "authen: one: "
            print self.item[res[0]]
            print map(self._map_func,res)
            return map(self._map_func,res)
#         except GlobalValueError:
#             self.rec(count)
        except:
            raise
            #raise RECRuntimeError(context_info="RandomNewsRecommender",debug_info=traceback.format_exc())
    


class BaysianMoviesRecommender(Recommender):
    """
        BaysianNewsRecommender recommends news based on Baysian framework.
    """
    def __init__(self,user_model,news_model):
        self.user=user_model
        self.item=news_model

    def _filter(self,token):
        return self.black_filter.is_ok(token)

    def _map_func(self,x):
        return self.item[(x[0])]

    def rec(self,count,cursor=0):
        """
            Attributes:
                count: recomending count.
                cursor:(cursor)*count--(cursor+1)*count items will be choose.
            Return the top N news that match user's interest.
            Fistly:     We need to fliter the news which has been read.
            Secondly:   Sum the socre which the news get in each feature.
                        and we will initiate an array with volume of n to
                        record the top n news on the fly.
            finally:    Return the corresponding news content based on the top
                        n's news id.

        """
        try:
            top_dict={}
            for model in self.item.get_model():
                sum=0.0
                for genres in model['genres']:
                    sum+=self.user['gen_model'][genres]
                sum=sum*(model['year']-1900)/200.0
                if model['ratings']>0:
                    top_dict[model['id']]=sum*math.log(model['ratings'])
                else:
                    top_dict[model['id']]=sum*math.log(20)
            top=list(top_dict.iteritems())
            top.sort(cmp=lambda x,y:cmp(y[1], x[1]))
            return map(self._map_func,top[(cursor*count):((cursor+1)*count)])
#         except GlobalValueError:
#             self.rec(count,cursor)
        except:
            raise
#             raise RECRuntimeError(context_info="BaysianNewsRecommender",debug_info=traceback.format_exc())


