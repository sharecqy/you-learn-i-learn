#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-10-8

@author: cqy
'''
import feedparser
import datetime
from decruft import Document
import urllib2
import jieba
import math
def truncate(s, length):
    if len(s) >= length:
        return s[:length]
    else:
        return s

class Article:
    """
    def __init__(self,title,description,publisheddate,itemurl,ranking,feedurl):
        self.title=title
        self.description=description
        self.publishedDate=publisheddate
        self.itemUrl=itemurl
        self.ranking=ranking
    """    
 
    def parse_Items(self,feedurl):
        feed=feedparser.parse(feedurl)
        index=0;
        #items=[]
        for entry in feed.entries:
            d={}
            d['itemurl'] = entry.get('link', None).encode('utf-8').strip()
            if d['itemurl'] == None:
                continue
            d['summary']=self.get_Summary(d['itemurl'])
            if d['summary'] == None:
                continue
            d['title'] = truncate(entry.get('title', '').encode('utf-8').strip(), 99)
            d['description']=entry.get('description','').encode('utf-8').strip()
            #content=entry.get('content','').encode('utf-8').strip()
            sequence_time = entry.get('updated_parsed', None) or entry.get('published_parsed', None)
            if sequence_time == None:
                d['publisheddate'] = datetime.datetime.now()
            else:
                d['publisheddate'] = datetime.datetime(*sequence_time[:6])
            d['ranking'] = index
            index = index+1
            d['feedurl'] = feedurl.encode('utf-8').strip()
            
            #items.append(d)
            yield d
    
    def get_Summary(self,itemurl):
        try:
            f = urllib2.urlopen(itemurl)
            return Document(f.read()).summary()#.encoding('utf-8')
        except:
            return None

       


class Tfidf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpusDict = {}
        self.features=[]

    def addDocument (self, docName, listOfWords):
        # building a dictionary
        docDict = {}
        length=0
        for w in listOfWords:
            length+=1
            if docDict.has_key (w):
                docDict [w] = docDict [w] + 1.0
            else:
                docDict [w] = 1.0
            if self.corpusDict.has_key (w):
                self.corpusDict [w] = self.corpusDict [w] + 1.0
            else:
                self.corpusDict [w] = 1.0

        # normalizing the dictionary
        for k in docDict:
            docDict [k] = docDict [k] / length

        # add the normalized document to the corpus
        self.documents.append ( [docName, docDict] )
    
    def setDocFeatures(self):
        """ idf=log((numofdoc)/(d contains word which is one of docs)"""
        
        for docName, docDict in self.documents:
            docFeature={}
            for key,tf in docDict.items():
                idf=math.log(len(self.documents)/self.corpusDict[key])
                docFeature[key]=tf*idf
            self.features.append([docName,docFeature])
            
    def getRankedFeaures(self):
        self.setDocFeatures()
        for docName, docDict in self.features:
            print docName
            count=10
            for key, value in sorted(docDict.iteritems(), key=lambda (k,v): (v,k),reverse=True):
                print key.encode('utf-8'), value
                count-=1
                if count==0:break
     
    def similarities (self, listOfWords):
        """Returns a list of all the [docname, similarity_score] pairs relative to a list of words."""

        # building the query dictionary
        queryDict = {}
        for w in listOfWords:
            if queryDict.has_key (w):
                queryDict [w] = queryDict [w] + 1.0
            else:
                queryDict [w] = 1.0

        # normalizing the query
        length = float (len (listOfWords))
        for k in queryDict:
            queryDict [k] = queryDict [k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            docDict = doc [1]
            for k in queryDict:
                if docDict.has_key (k):
                    score += (queryDict [k] / self.corpusDict [k]) + (docDict [k] / self.corpusDict [k])
            sims.append ([doc [0], score])

        return sims


class Analysis:
    def __init__(self):
        self.article=Article().parse_Items("http://news.google.com/news?ned=us&topic=h&output=rss")  
        
    def parse_Word(self,content):
        return jieba.cut(content)
    
    def tfidf(self):
        analyser=Tfidf()
        for a in self.article:
            analyser.addDocument(a['title'], self.parse_Word(a['summary']))
        analyser.getRankedFeaures()    
        
ana=Analysis()
ana.tfidf()

class tanslate:
    pass














class Feed:
    """
    def __init__(self,feedurl,site,title,description,category,topic,prior,properity):
        self.feedUrl=feedurl                
        self.siteUrl=site
        self.title=title
        self.description=description
        self.category=category                      #sports,finance,technology
    """
        
    def paser_Feed(self,feedurl):
        feed=feedparser.parse(feedurl)
        d = {}
        d["feedurl"] = feedurl
        d["title"] = feed.feed.get('title', u"").encode('utf-8').strip()
        d["siteurl"] = feed.feed.get('link', u"").encode('utf-8').strip()
        d["description"] = feed.feed.get('subtitle', u"").encode('utf-8').strip()
        d["category"]="".encode('utf-8').strip()
        return d
    
