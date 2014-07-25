class BaseError(Exception):
	def __init__(self,context_info="",debug_info=""):
		self._context_info=context_info
		self._debug_info=debug_info

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "\nError:%s\nContext_info:%s\nDebug_info:%s" %(self.__class__.__name__,self._context_info,self._debug_info)



class DBError(BaseError):
	pass

class UserRequestError(BaseError):
	pass

class RECRuntimeError(BaseError):
	pass

class HandlerRuntimeError(BaseError):
	pass

class GlobalValueError(BaseError):
	"""
        The global object like News object is updated periodically,so,it's not thread safe.
        In this case we need to raise this Error and redo the recommendation.
    """
	pass
