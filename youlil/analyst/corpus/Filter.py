'''
Created on 2012-10-24

@author: cqy
'''

# Filters

class Filter(Composable):
    """Base class for Filter objects. A Filter subclass must implement a
    filter() method that takes a single argument, which is an iterator of Token
    objects, and yield a series of Token objects in return.

    Filters that do morphological transformation of tokens (e.g. stemming)
    should set their ``is_morph`` attribute to True.
    """

    def __eq__(self, other):
        return other and self.__class__ is other.__class__

    def __call__(self, tokens):
        raise NotImplementedError

class PassFilter(Filter):
    """An identity filter: passes the tokens through untouched.
    """

    def __call__(self, tokens):
        return tokens
