
from web.handlers.base import BaseRequestHandler
import tornado.web
from tornado.web import asynchronous
from tornado import gen
import random
"""
	User handle is to deal with user's profile including (personal index,profile,words book)
"""


class UserIndexHandler(BaseRequestHandler):
    """
       
    """
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def get(self):
        visiting_user_id=self.current_user
        visited_user_id=self.get_argument('uid',visiting_user_id)
    	request1,request2,request3=yield [gen.Task(self.db.topic.find,{'user_id':visited_user_id},limit=3),
                                          gen.Task(self.db.user.find_one,{'_id':float(visited_user_id)},fields={'_id':1,'username':1}),
                                          gen.Task(self.db.user.find,{'_id':{'$ne':float(visiting_user_id)}},limit=100,fields={'_id':1,'username':1})]
        topics=request1[0][0]
        
        visited_user=request2[0][0]
        if visited_user_id!=visiting_user_id:
            visited_user['addable']=True;
        else:
            visited_user['addable']=False;
        rec_users=request3[0][0]
        print len(rec_users)
        rec_users=random.sample(rec_users,3)
        for topic in topics:
            topic['comments_num']=len(topic['comments'])
            topic['votes_num']=topic['statistic']['push']-topic['statistic']['pull']
        context=self.get_context({'visited_user':visited_user,'rec_users':rec_users,'topics':topics})
        self.write(self.render.mypage(context))
        self.finish()

    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
    	pass




class AccountSettingHandle(BaseRequestHandler):
    """
       
    """
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def get(self):
    	pass

    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
    	pass


