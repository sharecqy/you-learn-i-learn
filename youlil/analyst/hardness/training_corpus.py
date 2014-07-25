from pymongo import Connection, DESCENDING
from nltk.tokenize import RegexpTokenizer,sent_tokenize,word_tokenize
from random import choice
class MongoDBSequence:
    """
        Generate Training Corpus
    """   
    def __init__(self,host='localhost',port=27017,db='learner',collection='news'):
        self.conn=Connection(host,port)
        self.collection=self.conn[db][collection]
        self.data=self._get_data()

    def __len__(self):
        return self.collection.count()

    def _get_data(self):
        res=self.collection.find()
        for item in res:
            yield item

    def __iter__(self):
        return self

    def next(self):
        #f=lambda d:d.get(field)$
        return self.data.next()

class RandomSentence:
    """
        Generate Training Corpus
    """   
    def __init__(self,sent_num=10):
        self._seq=MongoDBSequence()
        self.sent_num=sent_num
        self._data=self._sents()
    
    def __len__(self):
        return self.sent_num

    def __iter__(self):
        return self
    
    def next(self):
        return self._data.next()

    def _sents(self):
        count=0
        for doc in self._seq:
            if count==self.sent_num:
                raise StopIteration()
            temp=sent_tokenize(doc['text_snacktory'])
            sent=choice(temp)
            if len(sent)<8:continue
            count+=1
            yield sent
