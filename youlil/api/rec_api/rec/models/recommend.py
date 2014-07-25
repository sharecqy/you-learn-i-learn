#!/usr/bin/env python
# coding: utf-8

import random
from rec.models.filter import BlackListFilter
from rec.utils.topnlist import TopNList
from rec.models.error import RECRuntimeError,GlobalValueError
import traceback
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
    
    
class RandomNewsRecommender(Recommender):
    """
        RandomNewsRecommender recommend news randomly.
    """
    def __init__(self,item_model,user_model):
        self.item=item_model
        if user_model:
            self.black_set=set(user_model['readlist'])
        else:
            self.black_set=[]

        print self.black_set

    def _map_func(self,x):
        return self.item[(x,True)]

    def rec(self,count):
        """
            RandomNewsRecommender randomly recommend news except ones user has read,
            but in term of speed we introduce a control variable to avoid looping
            too long(it may include some read news finally,it's not important).
            The method ends in (count+control) times loop.
        """
        try:
            cands=set(self.item.get_ids()).difference(self.black_set)
            print "Get in Recommender!!!!!!!!!!!"
            print len(cands)
            print cands
            if len(cands)<count:
                res=random.sample(self.item.get_ids(),count)
            else:
                res=random.sample(cands,count)
            print "map: "
            print map(self._map_func,res)
            return map(self._map_func,res)
        except GlobalValueError:
            self.rec(count)
        except:
            raise
            raise RECRuntimeError(context_info="RandomNewsRecommender",debug_info=traceback.format_exc())
    


class BaysianNewsRecommender(Recommender):
    """
        BaysianNewsRecommender recommends news based on Baysian framework.
    """
    def __init__(self,user_model,news_model):
        self.user=user_model
        print "Baysian!!!!!"
        print user_model['readlist']
        self.item=news_model
        self.black_filter=BlackListFilter(user_model['readlist'])

    def _filter(self,token):
        return self.black_filter.is_ok(token)

    def _map_func(self,x):
        return self.item[(x[0],False)]

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
            top=TopNList(n=count*(cursor+1),value_func=(lambda x:x[1]))
            for index,nm in enumerate(self.item.get_model()):
                if self._filter(nm[0]):
                    sum=self.user['cat_model'][nm[1]]+self.user['rss_model'][nm[2]]
                    top.append((index,sum))
            return map(self._map_func,top[(cursor*count):((cursor+1)*count)])
        except GlobalValueError:
            self.rec(count,cursor)
        except:
            raise
            raise RECRuntimeError(context_info="BaysianNewsRecommender",debug_info=traceback.format_exc())


