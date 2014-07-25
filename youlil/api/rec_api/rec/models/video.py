'''
Created on June 14, 2013

@author: unclelee
'''
from rec_api.rec.models.basic import Model


import numpy as np
class VideoModel(Model):
    """
            Raw Data(which is put in a python dict):
                
    """
    def  _format_model(self,*args,**kwargs):
        raise NotImplementedError("cannot instantiate Abstract Base Class")
    
    def __repr__(self):
        return "This video model is %s" %self.__class__.__name__

class PlainVideoModel(VideoModel):
    """
            Model elements:
                1._id (int)
                2.view_count (int)
                3.comment_count (int) 
                4.up_count (int)
                5.down_count (int)
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
        for video in res:
            model = {}
            model['id']=video['_id']
            ids.append(video['_id'])
            model['view_count']=video['view_count']
            model['comment_count']=video['comment_count']
            model['up_count']=video['up_count']
            model['down_count']=video['down_count']
            tags=video['tags']
            video['tags']=tags.split(',')
            data[video['_id']]=video
            models.append(model)
        return data,models,ids 
     
    def get_model(self):
        return self._model

    def get_ids(self):
        return self.ids