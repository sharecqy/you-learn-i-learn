'''
Created on 2012-11-12

@author: cqy
'''
import unittest
from model import Article_Generator

class Test(unittest.TestCase):


    def setUp(self):
        print "test start!"


    def tearDown(self):
        print "test end!"


    def test_ariticle_generator(self):
        ag=Article_Generator()
        articles=ag.get_articles_bycount(5, 'en')
        print len(articles)
        for index,art in enumerate(articles):
            print "article\t%d" %index 
            print "title:",art["title"]
            print "link:",art["url"]
            print "description:",art["description"]
            print 
        assert len(articles)==5,"incorrect list size"

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Test("test_ariticle_generator"))
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    s=suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
