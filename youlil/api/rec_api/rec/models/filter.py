#!/usr/bin/env python
# coding: utf-8

class Filter:
    """
        A Filter object is to judge a token whether is ok to pass.
    """
    def __init__(self):
        raise NotImplementedError("cannot instantiate Abstract Base Class")
    
    def is_ok(self,token):
        return True
    
class BlackListFilter(Filter):
    """
        Check a token based on a black_list.
    """
    def __init__(self,black_list):
        self.black_list=black_list
        
    def is_ok(self,token):
        if token in self.black_list:
            return False
        else:
            return True

