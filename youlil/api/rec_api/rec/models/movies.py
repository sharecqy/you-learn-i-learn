'''
Created on May 15, 2013

@author: unclelee
'''
from rec_api.rec.models.basic import Model
from rec_api.rec.settings import gen_dict

import numpy as np
class MoviesModel(Model):
    """
            Raw Data(which is put in a python dict):
                1.movie_id (int)
                2.genres (list of strings)
                3.ratings (dict)
                4.title (string)
                5.year (int)
                6.synopsis (string)
                7.posters(list of strings)
    """
    def  _format_model(self,*args,**kwargs):
        raise NotImplementedError("cannot instantiate Abstract Base Class")
    
    def __repr__(self):
        return "This movies model is %s" %self.__class__.__name__

class PlainMoviesModel(MoviesModel):
    """
            Model elements:
                1.movie_id (int)
                2.genres_id (list of integer)
                3.ratings (int) 
                4.year
    """
    def __init__(self,res):
        self._data,self._model,self.ids=self._format_model(res)
        
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, key):
        return self._data[key]
        
    def _format_model(self,res):
        data={}
        ids=[]        
        models=[]
        for movie in res:
            model = {}
            model['genres']=[]
            model['id']=movie['id']
            ids.append(movie['id'])
            model['ratings']=(movie['ratings']['audience_score']+movie['ratings']['critics_score'])/2
            model['year']=movie['year']
            data[movie['id']]=movie
            for genres in movie['genres']:
                model['genres'].append(gen_dict[genres])
            models.append(model)
        return data,models,ids 
     
    def get_model(self):
        return self._model

    def get_ids(self):
        return self.ids