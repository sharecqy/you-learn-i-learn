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
    
    
class RandomVideoRecommender(Recommender):
    """
        RandomNewsRecommender recommend news randomly.
    """
    def __init__(self,item_model):
        self.item=item_model
        

    def _map_func(self,x):
        return self.item[(x)]

    def rec(self,count):
        """
            RandomVideoRecommender randomly recommend news except ones user has read,
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