from hotqueue import HotQueue
LOGCONFIG="./config/log.cfg"
QUEUE=HotQueue("youlil", host="localhost", port=6379, db=9)
QUEUE_MOVIE=HotQueue("youlil_movie",host="localhost",port=6379,db=9)
