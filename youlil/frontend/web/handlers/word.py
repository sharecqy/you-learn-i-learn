from web.handlers.base import BaseRequestHandler
import tornado.web
from tornado.web import asynchronous
from tornado import gen
from tornado.httpclient import AsyncHTTPClient,HTTPRequest

"""
	In order to help user to remember word easily,we will provide four functions.
		1.query the definition of a word
		2.adding,deleting,visiting,downloading the word in personal words book
		3.you have lots of chance to write English in our website,we will record the words you have used.
		4.recommending words to the user.
"""
class QueryWordHandler(BaseRequestHandler):
    """
        This handler is to return user's personal page
        which contains some recommended news articles
    """   
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def get(self):
    	pass



class AddWordHandler(BaseRequestHandler):
	"""
	"""
	@asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
    	pass

class DeleteWordHandler(BaseRequestHandler):
	"""
	"""
	@asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
    	pass

class VisitWordHandler(BaseRequestHandler):
 	"""
 	"""
 	@asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def get(self):
    	pass


class RecordWordHandler(BaseRequestHandler):
  	"""
	"""
	@asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
    	pass

class DeleteRecordedWordHandler(BaseRequestHandler):
  	"""
	"""
	@asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
    	pass