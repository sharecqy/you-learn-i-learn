import tornado.web
from tornado.web import asynchronous
from tornado import gen
from web.handlers.base import BaseRequestHandler
from bson.son import SON
import datetime
import time
import markdown2
"""
	This topic module is to provide some functions to let users communicate or discuss topics.
	user could add a topic,vote a topic,comment a topic,tag a topic,revise other user's topic(help
	others write better English).
"""



class TopicIndexHandler(BaseRequestHandler):
    @property
    def hottest_topics(self):
        self._ht=self.settings['cached']['hottest_topic'].get_data()
        return self._ht

    """
        This topic index handler will response the request about topic.
        we can have different methods of ranking.
        1.time && voting
        2.Popularity 
        3.tag based recommendation
        4.new topic
        so forth
                        
    """
    @asynchronous
    @gen.engine
    def get(self):
        next,page_num=(self.get_argument('next',2),
                        self.get_argument('pg',0))
        if next=="0":page_num=max(0,int(page_num)-1)
        if next=="1":page_num=int(page_num)+1
    	response=yield gen.Task(self.db.topic.find,{},skip=page_num*20,limit=20,
                sort=[("time_index",-1)],fields={'title':1,'content':1,'username':1,'comments':1,'tags':1,'statistic':1})
        topics= response[0][0]
        #print topics
        user={'username':self.session.get('username')}
        for topic in topics:
            topic['comments_num']=len(topic['comments'])
            #topic['vote_num']=topic['statistic']['push']-topic['statistic']['pull']
            #self.cache.setex('tp'+topic['_id'],{'push':topic['statistic']['push'],'pull':topic['statistic']['pull']},3600)
        if self.request.headers['User-Agent']!="Android":
            context=self.get_context({'user':user,'newest_topics':topics,'hottest_topics':self.hottest_topics,'page_num':page_num})
            self.write(self.render.topicindex(context))
        else:
            self.write({'topics':topics,'page_num':page_num})
        self.finish()

class TopicHandler(BaseRequestHandler):
    """
        This handler is to return the topic content given by a specific topic id.
        we will return:
        1.topic info
        2.comments info
    """
    @asynchronous
    @gen.engine  
    def get(self):
    	topic_id=self.get_argument('tp')
        response1,response2=yield [gen.Task(self.db.topic.find_one,{'_id':float(topic_id)},fields={'title':1,'content':1,'username':1,'tags':1,'statistic':1,'comments':1,'user_id':1}) ,
                        gen.Task(self.db.comment.find,{'topic_id':float(topic_id)},fields={'content':1,'username':1,'statistic':1})]
        topic=response1[0][0] 
        comments=response2[0][0]
        user={'username':self.session.get('username')}
        user_id=self.session.get('user')
        if user_id==topic["user_id"]:
            topic['editable']=True
        else:
            topic['editable']=False
        topic['content']=markdown2.markdown(topic['content'])
        topic['vote_num']=topic['statistic']['push']-topic['statistic']['pull']
        #for comment in comments:
        #    self.cache.setex('com'+comment['_id'],{'push':comment['push'],'pull':comment['pull']},1800)
        if self.request.headers['User-Agent']!="Android":
            context=self.get_context({'user':user,'topic':topic,'comments':comments})
            self.write(self.render.topic(context))
        else:
            self.write({'topic':topic,'comments':comments})
        self.finish()	


class AddTopicHandler(BaseRequestHandler):
    """
        A topic collection contains fields:
        0.Id
        1.category.
        2.title
        3.content
        4.tags
        5.posted time
        6.writer(user id,user name)
        7.statistic(comments num,push,pull)
        8.modification(content,time,writer)
        9.comments Ids    
        10.paid attention users
    """  
    @tornado.web.authenticated
    def get(self):
        category="test"#self.get_argument('category')
        user={'username':self.session.get('username')}
        context=self.get_context({'user':user,'category':category})
        self.write(self.render.addtopic(context))

    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
        title,content,category,tags=(self.get_argument('title'),
                                     self.get_argument('content'),
                                     self.get_argument('category'),
                                     self.get_argument('tags'))

        print title
        print content
        tags=tags.split()
        command = SON()
        command['findandmodify'] = 'autoincrease'
        command['query'] = { '_id' : "topic_id" }
        command['update'] = { '$inc': { 'seq': long(1) } }
        #command['new'] = True
        #command['upsert'] = True
        response1=yield gen.Task(self.db.command,
                                     command)

        topic_id=response1[0][0]['value']['seq']
        user_id=self.session.get('user')
        username=self.session.get('username')
        time1 = datetime.datetime.now()
        time2 = int(time.mktime(time1.timetuple()))
        response2=yield gen.Task(self.db.topic.insert,{"_id":topic_id,
                                                      "title":title,
                                                      "content":content,
                                                      "category":category,
                                                      "user_id":user_id,
                                                      "username":username,
                                                      "statistic":{"comment":0,"push":0,"pull":0},
                                                      "posted_time":time1,
                                                      "time_index":time2,
                                                      "comments":[],
                                                      "tags":tags,
                                                      "careusers":[],
                                                      })
        self.redirect('/topicindex')

class EditTopicHandler(BaseRequestHandler):
    """
       
    """
    @asynchronous
    @gen.engine   
    @tornado.web.authenticated
    def get(self):
        topic_id=self.get_argument('tp')
        response=yield gen.Task(self.db.topic.find_one,{'_id':float(topic_id)}) 
        topic=response[0][0] 
        print response
        print topic
        if len(topic):
            user={'username':self.session.get('username')}
            context=self.get_context({'user':user,'topic_id':topic['_id'],'title':topic['title'],
                                        'content':topic['content'],'category':topic['category'],'tags':' '.join(topic['tags'])})
            self.write(self.render.edittopic(context))
            self.finish()
        else:
            self.redirect(''.join(['/topic?tp=',topic_id]))
        
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
        topic_id,title,content,tags=(self.get_argument('tp'),
                                        self.get_argument('title'),
                                        self.get_argument('content'),
                                        self.get_argument('tags'))

        tags=tags.split()
        response=yield gen.Task(self.db.topic.update,{"_id":float(topic_id)},
                                                     {"$set":{"title":title,"content":content,"tags":tags}})

        self.redirect(''.join(['/topic?tp=',topic_id]))
        

class DeleteTopicHandler(BaseRequestHandler):
    """
       
    """
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
        pass

class VoteTopicHandler(BaseRequestHandler):
    """
        This handler is to handle the voting from user.
        Key problem is how to limit a user's voting time for a given topic or comments
    """
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
    	topic_id,comment_id,push=(self.get_argument('tp',''),
                             self.get_argument('com',''),
                             self.get_argument('push',0))     

        if topic_id:
            voted_tp=self.session.get('voted_tp',[])
            if topic_id in voted_tp:
                self.write('voted')
            else:
                if len(voted_tp)>20:
                    voted_tp=voted_tp[10:]
                voted_tp.append(topic_id)
                self.session.set('voted_tp',voted_tp)
                if push:
                    response=yield gen.Task(self.db.topic.update,{"_id":float(topic_id)},
                                                     {"$inc":{"statistic.push":int(1)}})
                else:
                    response=yield gen.Task(self.db.topic.update,{"_id":float(topic_id)},
                                                    {"$inc":{"statistic.pull":int(1)}})
                self.write('ok')

        else:
            self.write('voted')        
        self.finish()

class VoteCommentHandler(BaseRequestHandler):
    """
        This handler is to handle the voting from user.
        Key problem is how to limit a user's voting time for a given topic or comments
    """
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
        comment_id,push=(self.get_argument('com',''),
                         self.get_argument('push',0))
        if comment_id:
            voted_com=self.session.get('voted_com',[])
            if comment_id in voted_com:
                self.write('voted')
            else:
                if len(voted_com)>20:
                    voted_com=voted_com[10:]
                voted_com.append(comment_id);
                self.session.set('voted_com',voted_com)
                if push:
                    response=yield gen.Task(self.db.comment.update,{"_id":float(comment_id)},
                                                     {"$inc":{"statistic.push":int(1)}})
                else:
                    response=yield gen.Task(self.db.comment.update,{"_id":float(comment_id)},
                                                     {"$inc":{"statistic.pull":int(1)}})
                self.write('ok')
        else:
            self.write('voted')
        self.finish()

class AddTPCommentHandler(BaseRequestHandler):
    """
        comments        0.comment Id
                        1.content
                        2.writer(user id,user name)
                        3.comment time
                        4.modification(list[time,write,content])
                        7.statistic(reply num,push,pull)
                        8.topic Id
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
        topic_id,comment=(self.get_argument('tp'),
                          self.get_argument('comment'))
        print comment
        command = SON()
        command['findandmodify'] = 'autoincrease'
        command['query'] = { '_id' : "comment_id" }
        command['update'] = { '$inc': { 'seq': long(1) } }
        #command['new'] = True
        #command['upsert'] = True
        response1=yield gen.Task(self.db.command,
                                     command)

        comment_id=response1[0][0]['value']['seq']
        user_id=self.session.get('user')
        username=self.session.get('username')
        time1 = datetime.datetime.now()
        time2 = int(time.mktime(time1.timetuple()))
        request2,request3=yield [gen.Task(self.db.topic.update,{'_id':float(topic_id)},{'$push':{'comments':comment_id}}),
                                 gen.Task(self.db.comment.insert,{'_id':comment_id,
                                                                   'content':comment,
                                                                   'user_id':user_id,
                                                                   'username':username,
                                                                   "statistic":{"push":0,"pull":0},
                                                                   'comment_time':time1,
                                                                   'time_index':time2,
                                                                   'modif':[],
                                                                   'topic_id':float(topic_id),
                                                                   })]
        self.redirect(''.join(['/topic?tp=',topic_id]))

class EditCommentsHandler(BaseRequestHandler):
    """
       
    """
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
        pass

class DeleteCommentsHandler(BaseRequestHandler):
    """
       
    """
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def post(self):
        pass


class ReviseHandler(BaseRequestHandler):
    """
    """
    @asynchronous
    @gen.engine    
    @tornado.web.authenticated
    def get(self):
    	pass
