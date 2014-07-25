import unittest
from rec_api.rec.utils.topnlist import TopNList 
class TestTopNList(unittest.TestCase):
    """
        CachedData provides a reload method which can be reload data
        periodically by ioloop.
        The unit test case here is to test the function of reload method. 
    """
    def setUp(self):
        self.data1=[2,4,5,1,5,7,1,12,43,523]
        self.data2=[(5,23),(12,5),(234,677),(454,121),(-112,0),(-1221,-23),(23,90),(12,99),(0,0)]

    def tearDown(self):
        pass
     
    def test_data1(self):
        self.atestfunc(data=self.data1,n=100,reverse=False,func=(lambda x:x))
        self.atestfunc(data=self.data1,n=10,reverse=False,func=(lambda x:x))
        self.atestfunc(data=self.data1,n=3,reverse=False,func=(lambda x:x))

        self.atestfunc(data=self.data1,n=100,reverse=True,func=(lambda x:x))
        self.atestfunc(data=self.data1,n=10,reverse=True,func=(lambda x:x))
        self.atestfunc(data=self.data1,n=3,reverse=True,func=(lambda x:x))

    def test_data2(self,):
        self.atestfunc(data=self.data2,n=200,reverse=True,func=(lambda x:x[1]))
        self.atestfunc(data=self.data2,n=30,reverse=True,func=(lambda x:x[1]))
        self.atestfunc(data=self.data2,n=1,reverse=True,func=(lambda x:x[1]))

        self.atestfunc(data=self.data2,n=200,reverse=False,func=(lambda x:x[1]))
        self.atestfunc(data=self.data2,n=30,reverse=False,func=(lambda x:x[1]))
        self.atestfunc(data=self.data2,n=1,reverse=False,func=(lambda x:x[1]))

    def atestfunc(self,data,n,reverse,func):    
        func=func
        top=TopNList(n=n,reverse=reverse,value_func=func)
        for item in data:
            top.append(item)
        count=n if len(data)>n else len(data)
        self.assertEqual(len(top),count)

        ranked=sorted(data,key=func,reverse=not reverse)

        for i in range(count):
            self.assertEqual(func(top[i]),func(ranked[i]))
        #print "ranked",ranked
        #print "top   ",top._data


if __name__ == '__main__':
    unittest.main()

