import datetime,time

class Votable(object):
	pass


class TopicRanking(object):
	def __init__(self,g):
		self.g=g

	def sort(self,topics):
		now= int(time.mktime(datetime.datetime.now().timetuple()))
		for tp in topics:
			tp['para']=(tp['comments_num']+float(tp['statistic']['push']-tp['statistic']['pull']-1))/pow((now-tp['time_index'])/3600+2,self.g)
		topics=sorted(topics,key=lambda tp:tp['para'],reverse=True)
                #for tp in topics:
                #    print tp['para']," ",tp['comments_num']," ",tp['statistic']['push']," ",tp['statistic']['pull']," ",(now-tp['time_index'])/3600
		return topics
