from web.handlers.base import BaseRequestHandler,authenticated
from web.settings import REC_MOV_URL,REC_WEEKLY_URL
import tornado.web
from tornado.web import asynchronous
from tornado import gen
from tornado.httpclient import AsyncHTTPClient,HTTPRequest
import cPickle
import urllib
import simplejson as json
from bson.son import SON
import random
import datetime
import time
rec_count=6
class MovieIndexHandler(BaseRequestHandler):
    """
        This handler is to return user's personal page
        which contains some recommended movies
    """   
    @asynchronous
    @gen.engine    
    def get(self):
        user_id=self.current_user
        cursor=self.get_argument('cursor',0)
        authenticated=self.isAuthenticated()
        watched=self.session.get('watched',[])
        client=AsyncHTTPClient()
        req_dict={'authenticated':authenticated,'user_id':user_id,'cursor':cursor,'watched':cPickle.dumps(watched)}
        """Request for recommendation"""
        request=HTTPRequest(url="%s?%s" %(REC_MOV_URL,urllib.urlencode(req_dict)),
                            method="GET")
        response=yield gen.Task(client.fetch,request)
        print "response: "
        print response
        movies=json.loads(response.body)['rec']
        """Request for weekly topics"""
        req_dict_weekly={'user_id':user_id}
        request_weekly=HTTPRequest(url="%s?%s" %(REC_WEEKLY_URL,urllib.urlencode(req_dict_weekly)),
                            method="GET")
        response_weekly=yield gen.Task(client.fetch,request_weekly)
        weekly_movies=json.loads(response_weekly.body)['rec']
        """Get user name"""
        user={'username':self.session.get('username')}
        """Return the params to the client"""
        context=self.get_context({'movies':movies,'user':user,'weekly':weekly_movies})
        self.write(self.render.movieindex(**context))
        self.finish()


    @asynchronous
    @gen.engine    
    def post(self):
        user_id=self.current_user
        cursor=self.get_argument('cursor',0)
        watched=self.session.get('watched',[])
        authenticated=self.isAuthenticated()
        if authenticated==0:
            self.write({'redirect':self.get_login_url()})
        else:
            client=AsyncHTTPClient()
            req_dict={'authenticated':authenticated,'user_id':user_id,'cursor':cursor,'watched':cPickle.dumps(watched)}
            request=HTTPRequest(url="%s?%s" %(REC_MOV_URL,urllib.urlencode(req_dict)),
                                method="GET")
            response=yield gen.Task(client.fetch,request)
            print "response: "
            print response
            self.write({'rec':json.loads(response.body)['rec']})
        self.finish()
        
class MovieHandler(BaseRequestHandler):
    """
        This handler is to return a news article's full text to user
    """
    @asynchronous
    @gen.engine    
    def get(self):
        user_id=self.current_user
        movie_id=self.get_argument('mid')        
        response1,response2=yield [gen.Task(self.db.movie.find_one,{'id':int(movie_id)}),
                                    gen.Task(self.db.movie_comment.find,{'movie_id':float(movie_id)},fields={'content':1,'username':1,'statistic':1,'comment_time':1})]
        self.movie=response1[0][0]
        self.comments=response2[0][0]
        self.user={'user_id':user_id,'username':self.session.get('username')}
        context=self.get_context({'movie':self.movie,'comments':self.comments,'user':self.user})
        self.write(self.render.movie(**context))
        self.finish()
        
    def post(self):
        pass

    def on_finish(self):
        """
            Record user's recently watched movies,then we can filter them 
            out in the recommendation
        """
        if self.isAuthenticated():
            watched=self.session.get('watched',[])
            watched.append(self.movie['id'])
            """  keep the session in a limited size"""
            if len(watched)>50:watched=watched[25:]
            self.session.set('watched',watched)
            data=list(self.movie['genres'])
            """Put user's log in a queue"""                
            self.queue.put({'type':'click',
                            'user_id':self.user['user_id'],
                            'genres_list':data
                            })
    @property
    def queue(self):
        self._queue=self.settings['queue_movie']
        return self._queue


class AddMovieCommentsHandler(BaseRequestHandler):
    """
        movie_comments:        0.movie_comment Id
                               1.content
                               2.writer(user id,user name)
                               3.comment time
                               4.modification(list[time,write,content])
                               7.statistic(reply num,push,pull)
                               8.movie Id

    """
    @asynchronous
    @gen.engine    
    @authenticated
    def post(self):
        """
            This handler get the comments from users, and then insert to database
        """
        movie_id,comment=(self.get_argument('mid'),
                          self.get_argument('comment'))
        print movie_id
        print comment
        command = SON()
        command['findandmodify'] = 'autoincrease'
        command['query'] = { '_id' : "movie_comment_id" }
        command['update'] = { '$inc': { 'seq': long(1) } }

        response1=yield gen.Task(self.db.command,
                                     command)

        comment_id=response1[0][0]['value']['seq']
        user_id=self.session.get('user')
        username=self.session.get('username')
        time1 = datetime.datetime.now()
        time2 = int(time.mktime(time1.timetuple()))
        request2=yield gen.Task(self.db.movie_comment.insert,{'_id':comment_id,
                                                         'content':comment,
                                                         'user_id':user_id,
                                                         'username':username,
                                                         "statistic":{"push":0,"pull":0},
                                                         'comment_time':time1,
                                                         'time_index':time2,
                                                         'modif':[],
                                                         'movie_id':float(movie_id),
                                                       })
        self.redirect(''.join(['/movie?mid=',movie_id]))
