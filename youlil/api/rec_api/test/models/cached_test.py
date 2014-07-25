#!/usr/bin/env python
# coding: utf-8

import unittest
from rec_api.rec.models.cached import Candidate,Trend 
class TestCachedData(unittest.TestCase):
    """
        CachedData provides a reload method which can be reload data
        periodically by ioloop.
        The unit test case here is to test the function of reload method. 
    """
    def setUp(self):
        self.candidate=Candidate(400)
        self.trend=Trend()

    def shutdown(self):
        pass
     
    def test_candidate(self):
        self.candidate.reload()
        self.assertEqual(len(self.candidate.get_data().get_data()),400)
    
    
    def test_trend(self):
        self.trend.reload()
        print self.trend.get_data()


if __name__ == '__main__':
    unittest.main()

