from web.handlers.base import BaseRequestHandler
import hashlib
import tornado.web
from tornado.web import asynchronous
from tornado import gen
from bson.son import SON

class LoginIndexHandler(BaseRequestHandler):
    """
        This handler supports the index page that a user views at its first
        time coming to the site.
        *functions*
            Hottest news:a brief view of our site(The service we provide).    
            Login
            signup            
    """
    def get(self):
        context=self.get_context({"index_image":"static/images/novel_trip.jpg"})
        self.write(self.render.index(**context))

class LoginHandler(BaseRequestHandler):
    """
    def get(self):
        if self.session.get('login')==1:
            self.redirect('/myindex')
            return
        self.write(self.render.login(**self.get_context()))
    """
    def get(self):
        signup=self.get_argument('signup',0)
        if signup:
            login_state="invisible"
            signup_state="visible"
        else:
            login_state="visible"
            signup_state="invisible"
        context=self.get_context({"login_state":login_state,"signup_state":signup_state,"index_image":"static/images/novel_trip.jpg"})
        self.write(self.render.login(**context))
        
    @asynchronous
    @gen.engine        
    def post(self):
        email = self.get_argument('login_email')
        password = self.get_argument('login_password')
        response=yield gen.Task(self.db.user.find_one,{'email':email})     
        vali,msg,user=self._validate(email, password,response) 
        print 'here ',vali,msg,user
        if vali:
            print self.session
            print user['_id']
            self.session.set('user', user['_id'])
            self.session.set('username', user['username'])
            self.session.set('login',1)
            print self.session.get('user')
            self.write("success")
        else:
            self.write(msg)
            self.set_status(400)
        print self.session.get('user')
        self.finish()
    
   
    def _validate(self,email,password,response): 
        user=response[0][0]
        if not email or not password or response[1]['error'] or not len(response[0][0]):
            return False,"User doesn't exist",""
        if  self._password_generate(password)==user['password']:
            return True,"Login Success",user
        else:
            return False,"Password is Wrong",""
        
    def _password_generate(self,password):
        return hashlib.sha1("cqy'sXiaoGuiKer"+password).hexdigest()


class RegisterHandler(BaseRequestHandler):
    def get(self):        
        self.write(self.render.register(**self.render_params))
        
    @asynchronous
    @gen.engine  
    def post(self):
        email,username,password1,password2=(self.get_argument('signup_email'),
                                            self.get_argument('signup_name'),
                                            self.get_argument('signup_password'),
                                            self.get_argument('signup_passconf'),)
        vali,msg=self._pre_validate(email,username,password1,password2)
        if not vali:
            self.write(msg)
            return        
        response1=yield gen.Task(self.db.user.find_one,{'email':email})
        vali,msg=self._existed_validate(email,response1)
        if vali:
            command = SON()
            command['findandmodify'] = 'autoincrease'
            command['query'] = { '_id' : "user_id" }
            command['update'] = { '$inc': { 'seq': long(1) } }
            #command['new'] = True
            #command['upsert'] = True
            response2=yield gen.Task(self.db.command,
                                     command)
            
            user_id=response2[0][0]['value']['seq']
            response3=yield gen.Task(self.db.user.insert,{"_id":user_id,
                                                         "email":email,
                                                         "username":username,
                                                         "password":self._password_generate(password1)})
                      
            if response3[1]['error']:
                self.write("Login Failed caused by a system fail!")
                self.finish()
            else:
                self.session.set('user',user_id)
                self.session.set('username', username)
                self.session.set('login',1)
                self.redirect('/myindex')
        else:
            self.write(msg)
            self.finish()

        
    
    def _pre_validate(self,email,username,password1,password2):
        if not email:
            return False,"Email address can't be empty!"
        if not username:
            return False,"Username can't be empty"
        if password1!=password2:
            return False,"Two passwords are not identical!"
        if len(password1)<6:
            return False,"Password at least 6 letters"
        return True,"Success"
    
    def _existed_validate(self,email,response):       
        user=response[0][0]
        if len(user):
            return False,"This email has been used!"
        else:
            return True,""
        
    def _password_generate(self,password):
        return hashlib.sha1("cqy'sXiaoGuiKer"+password).hexdigest()
        
class LogoutHandler(BaseRequestHandler):
    def get(self):
        self.session.set('login',0)
        self.redirect('/')
             
