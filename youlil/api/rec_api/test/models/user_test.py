#!/usr/bin/env python
# coding: utf-8

import unittest
from rec_api.rec.models.user import BaysianUserModel 

class TestUserModel(unittest.TestCase):
    """
        CachedData provides a reload method which can be reload data
        periodically by ioloop.
        The unit test case here is to test the function of reload method. 
    """
    def setUp(self):
        pass
    def tearDown(self):
        pass
     
    def test_model1(self): 
        cat=5
        user_virtual_clicks=10
        trend_virtual_clicks=100
        user={0:5,1:5,2:5,3:5,4:5}
        trend={0:100,1:100,2:100,3:100,4:100}
        model=BaysianUserModel(cat,user,trend,user_virtual_clicks,trend_virtual_clicks).get_model()
        for x in model:
            self.assertEqual(x,1.0/5)
        print model

    def test_model2(self): 
        cat=3
        user_virtual_clicks=10
        trend_virtual_clicks=100
        user={0:1,1:5,2:10}
        trend={0:120,1:40,2:160}        
        model=BaysianUserModel(cat,user,trend,user_virtual_clicks,trend_virtual_clicks).get_model()

        """
            user_interest=[11.0/46,15.0/46,20.0/46]
            trend_interest=[220.0/620,140.0/620,260.0/620]

        """
        user_interest=[11.0/46,15.0/46,20.0/46]
        trend_interest=[220.0/620,140.0/620,260.0/620]
        real_model=[user_interest[i]*trend_interest[i] for i in range(len(user_interest))]
        model_sum=sum(real_model)
        real_model=[item/model_sum for item in real_model]

        for i in range(len(real_model)):
            self.assertEqual(model[i],real_model[i])
        print model
        print real_model

if __name__ == '__main__':
    unittest.main()

