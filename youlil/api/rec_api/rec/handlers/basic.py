import tornado.web

class BaseRequestHandler(tornado.web.RequestHandler):    
    def get_current_user(self):
        """Return user's id from user's request query item,otherwise,return a None"""
        user=self.get_argument('user_id')
        if user is None:
            return None
        return user

    @property
    def db(self):
        """ Return mongoddb client pool"""
        self._db=self.settings['db']
        return self._db
    
    @property
    def logger(self):
        self._logger=self.settings['logger']
        return self._logger
        
