#!/usr/bin/env python
# coding: utf-8
import unittest
from rec_api.rec.models.recommend import BaysianNewsRecommender
from rec_api.rec.models.user import BaysianUserModel
import numpy as np
class TestRecommender(unittest.TestCase):
    """

    """
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    """
    def test_rec(self):
        rss_model=np.array([0.1,0.3,0.2,0.4],dtype=float)
        cat_model=np.array([0.3,0.5,0.2],dtype=float)
        read=[2,5]
        news_model=np.array([[0,2,0,1],[1,2,0,2],[1,1,0,3]],dtype=float)
        recommender=BaysianNewsRecommender(read,)
    """
    def test_rec(self):
        cat_count=3
        rss_count=5
        user={"rss_clickmodel":{0:5,1:5,2:5,3:5,4:5},
              "cat_clickmodel":{0:10,1:10,2:10}}
        trend={"rss_clickmodel":{0:100,1:100,2:100,3:100,4:100},
               "cat_clickmodel":{0:200,1:200,2:200}}
        read=[3,5]

        #print "see",BaysianUserModel(rss_count,user['rss_clickmodel'],trend['rss_clickmodel']).get_model()
        #print "params",rss_count,user['rss_clickmodel'],trend['rss_clickmodel']
        #print "see",BaysianUserModel(cat_count,user['cat_clickmodel'],trend['cat_clickmodel']).get_model()



        class News:
            def __init__(self):
                self.news_model=np.array([[0,2,0,1],
                                         [1,2,0,2],
                                         [1,1,0,3],
                                         [2,1,0,4],
                                         [2,1,0,6],
                                         [2,1,0,7],
                                         [4,1,0,5]],
                                         dtype=float)
            def get_model(self):
                return self.news_model
        recommender=BaysianNewsRecommender(read,user,trend,News(),
                                           rss_count=rss_count,
                                           cat_count=cat_count)
        print recommender.rss_usermodel.get_model()
        print recommender.cat_usermodel.get_model()
        print list(recommender.rec(10))


if __name__ == '__main__':
    unittest.main()

