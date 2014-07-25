#!/usr/bin/env python
# coding: utf-8

from rec_api.rec.settings import rss_dict
from rec_api.rec.models.basic import Model
from rec_api.rec.models.error import GlobalValueError
import numpy as np
class NewsModel(Model):
    """
            NewsModel is a simplified way to represent kinds of news which is 
        typically represented by a vector.   
            When we retrieve raw news data from database which contains
        art_id,title,url,description,rss_id,pub_date,we need to convert
        them in a easier and more efficient format to match a particular
        user. 
            Raw Data(which is put in a python dict):
                1.art_id.
                2.title
                3.url
                4.description
                5.cat_name
                6.pub_date
    """
    def  _format_model(self,*args,**kwargs):
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def __repr__(self):
        return "This news model is %s" %self.__class__.__name__

class PlainNewsModel(NewsModel):
    """
           This is a easy and directly newsmodel.when we do recommendation,
        only news's category,rss source and reading hardness are necessary.
        As a result,we convert each news as a vector consisting of that 
        three elements which are put in a numpy array..
            Model elements:
                1.news id
                2.news category
                3.rss source 
                4.reading hardness
    """
    def __init__(self,res):
        self._data,self._model,self._map_table=self._format_model(res)

    def __getitem__(self, key):
        if key[1]:
            #convert art_id to index
            try:
                index=self._map_table[key[0]]
            except KeyError:
                """
                    The Global object like News object is updated periodically,
                    so,it's not thread safe.In this case we need to raise 
                    GolbalValueError and redo the recommendation.
                """
                raise GlobalValueError()
        else:
            index=key[0]
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def _format_model(self,res):
        """
                We will divide raw data into two parts.First one is the model of 
            news,and second one is the meta information of news.The model is 
            stored in a numpy array.The meta is put in a python dict,and we 
            will give it a new index which the two parts are connected by.
                model:1.news index;2.news category;3.rss source;4.reading hardness
        """
        data={}
        map_table={}
        model=np.zeros((len(res),4),dtype=float)
        for index,news in enumerate(res):
            news['cat_name']=rss_dict[news['rss_id']][1]
            model[index]=[news['art_id'],rss_dict[news['rss_id']][0],news['rss_id'],news['hardness']]
            map_table[news['art_id']]=index
            del news['rss_id']
            del news['_id']
            data[index]=news
        return data,model,map_table
    
    def get_model(self):
        return self._model

    def get_ids(self):
        return self._map_table.keys()
        

    
    
    
    

        
