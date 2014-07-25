class Model(object):
    """
        Model is a simplified way to represent a user or item in real life 
        which is typically represented by a vector.    
    """
    def get_model(self):
        raise NotImplementedError("cannot instantiate Abstract Base Class")
    
    def __repr__(self):
        return "This model is %s" %self.__class__.__name__