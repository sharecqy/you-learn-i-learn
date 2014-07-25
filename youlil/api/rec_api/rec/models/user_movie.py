'''
Created on May 16, 2013

@author: unclelee
'''
from basic import Model
from rec.settings import GENRES_COUNT,GENRES_USER_VIRTUALCLICK

import numpy as np

class UserModel(Model):
    """
        UserModel is a simplified way to represent a user in real life 
        which is typically represented by a vector.    
    """
    def get_model(self):
        return self._user_model   

    def __repr__(self):
        return "This user model is %s" %self.__class__.__name__

class DimensionalUserModel(UserModel):
    """
        This user model contains mutli single user model.We can
        initiate them one by one (like a pipeline) and get each 
        of them with model name.
    """    
    def __init__(self):
        self._user_model={}

    def __getitem__(self,name):
        return self._user_model[name]  

    def init_watchedlist(self,watchedlist):
        self._user_model['watchedlist']=watchedlist
        return self

    def init_genresmodel(self,cat_length,user_clickmodel):
        self._user_model['gen_model']=BaysianUserModel(cat_length,user_clickmodel)
        return self

    def init_likeOrnotmodel(self):
        return self
    

class BaysianUserModel(UserModel):
    """
        BaysianUserModel is a easy model using Baysian framework
        to depict user's interest.This model is divided into two
        aspects,one is user's intrinsic interest based on user's 
        past click history distributed in different categories and 
        different rss sources,and another one is based on the 
        popularity of news trend.
        In order to handle the case that user's click count or trend's
        click count are insufficient,we introduce some amount of virtual
        clicks to keep the uncertain of the user's interest.
        For the convenience and efficiency of computing,we represent
        user model as a numpy array
    """
    def __init__(self,cat_length,user_clickmodel,
                 user_virtualclick=GENRES_USER_VIRTUALCLICK):
        self.user_virtualclick=user_virtualclick
        self._user_model=self._model(cat_length,user_clickmodel)

    def __getitem__(self,index):
        return self._user_model[index]    
            
    def _model(self,length,user_clickmodel):
        user_model=self._format_model(length,user_clickmodel,
                                      self.user_virtualclick)
        model=self._interest(user_model)
        return model
    
    def _format_model(self,length,clickmodel,virtual_click):
        array=np.zeros(length)
        print "click_model:"
        print clickmodel
        for i in range(length):
            array[i]=virtual_click+clickmodel.get(str(i),0)
        return array
    
    def _interest(self,user_model):
        user_model=user_model/sum(user_model)
        """normalize the model"""
        return user_model
