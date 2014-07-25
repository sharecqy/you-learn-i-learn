import tornado.web
import functools
from web.utils.session import SessionMixin
from web.settings import render_jinja2,SITE_URL

class BaseRequestHandler(tornado.web.RequestHandler, SessionMixin):
    def prepare(self):
        pass
    
    def on_finish(self):
        pass
    
    def get_current_user(self):
        user = self.session.get('user')
        login = self.session.get('login',0)
        print user,login,type(login)
        if  user is None or not login:
            return None
        return user

    def isAuthenticated(self):
        if not self.current_user:
            return 0
        return 1           
    
    @property
    def render(self):
        self._render=render_jinja2
        return self._render
    
    @property
    def db(self):
        self._db=self.settings['db']
        return self._db

    @property
    def cache(self):
        self._cache=self.settings['cache']
        return self._cache
    
    def get_context(self,kwargs=None):        
        self.context={'site':SITE_URL,
                      'title':'You Learn I Learn',
                      'xsrf_form_html':self.xsrf_form_html,
                      'isAuthenticated':self.isAuthenticated()}
        if kwargs:
            self.context.update(kwargs)
        return self.context

def authenticated(method):
    """Decorate methods with this to require that the user be logged in.
    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        print  self.session.get('login',0)
        if not self.current_user or  not self.session.get('login',0):
            print "authenticated no users!!!!!!!"
            url = self.get_login_url()
            self.redirect(url)
            return
        print "authenticated have users!!!!!!!!!"
        return method(self, *args, **kwargs)
    return wrapper    
