#initiate render
from utils.render import render_jinja
render_jinja2= render_jinja(
                     searchpath='./web/templates', #''.join( [root_path,'templates']),   # Set template directory.
                     encoding='utf-8', # Encoding.
        )
SITE_URL="http://110.76.40.188:8003"
REC_URL="http://127.0.0.1:9003/rec"
REC_MOV_URL="http://127.0.0.1:9003/rec_mov"
REC_VDO_URL="http://127.0.0.1:9003/rec_vdo"
REC_WEEKLY_URL="http://127.0.0.1:9003/rec_weekly"
#initiate application configuration
SETTINGS = dict(
            cookie_secret="32oEtellGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            xsrf_cookies=False,
            debug=True,
            login_url="/login",
            logout_url="/logout",
        )

#initiate  database configuration
import asyncmongo
db=asyncmongo.Client(pool_id='front_dbpool', host='127.0.0.1', 
                  port=27017, maxcached=5, 
                  maxconnections=10, dbname='learner')
SETTINGS['db']=db

#initiate session configuration
import redis
redis_pool = redis.ConnectionPool(max_connections=5,
                                  host='localhost', 
                                  port=6379)

session_config={
                'engine': 'redis',
                'storage': {
                    'connection_pool': redis_pool,
                    'db_sessions': 10,
                    'db_notifications': 11,
                            },
                'cookies': {
                    'expires_days': 120,
                            },
                }
from hotqueue import HotQueue
queue = HotQueue("youlil", host="localhost", port=6379, db=9)
queue_movie = HotQueue("youlil_movie",host="localhost",port=6379,db=9)

SETTINGS['session_config']=session_config
SETTINGS['queue']=queue
SETTINGS['queue_movie']=queue_movie

SETTINGS['cache']=redis.Redis(connection_pool=redis_pool,db=12)

#topic ranking gravity parameter
G=1.8

#db info
MONGO_HOST='127.0.0.1'
MONGO_DBNAME='learner'
MONGO_TOPICCOLLCTION='topic'
