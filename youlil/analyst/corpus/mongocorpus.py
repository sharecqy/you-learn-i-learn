'''
Created on 2012-10-24

@author: cqy
'''
from gensim import interfaces
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.textcorpus import TextCorpus
from pymongo import Connection, DESCENDING
import hashlib
import jieba
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer,sent_tokenize
from translate import split_tran

ENStopWords = set(stopwords.words('english'))
ZHStopWords = set()

lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer("[\w]+")

def init_Stopword(zh_fname="./data/zh_stopword.txt", en_fname="./data/en_stopword.txt"):
    f = open(zh_fname, 'r')
    for word in f.readline():
        ZHStopWords.add(unicode(word.strip()))
    f.close()
    f = open(en_fname, 'r')
    for word in f.readline():
        ENStopWords.add(unicode(word.strip()))
    f.close()



def zh_Tokenize(text):
    return jieba.cut(text, cut_all=False)

def en_Tokenize(text):
    return tokenizer.tokenize(text)

def sent_Tokenize(text):
    return sent_tokenize(text)



def lowcase_Filter(token):
    return token.lower()

def en_Stopword_Filter(token):
    if token in ENStopWords or len(token) < 3:
        return None
    else:
        return token   

def zh_Stopword_Filter(token):
    if token in ZHStopWords or len(token) < 2:
        return None
    else:
        return token
    
def lemm_Filter(token):
    return lemmatizer.lemmatize(token)

    


class MongoCorpus(TextCorpus):
    def __init__(self, dbname="learner", topic="topic", article="article",language="en", dictionary=None):        
        con = Connection()
        db = con[dbname]
        self.topic_col = db[topic]
        self.article_col = db[article]
        self.length = 0
        self.language=language
        init_Stopword()
        if dictionary != None:
            self.dictionary = dictionary
        else:
            self.dictionary = Dictionary(self.get_texts())
    
    def _get_topic(self, limit=10):
        lang=self.language.split('_')[0]
        res = self.topic_col.find({'language':lang}).sort('timeindex', DESCENDING).limit(limit)
        #xx=[]
        for r in res:
            md5 = hashlib.md5()
            md5.update(r['itemurl'])
            article = self.article_col.find_one({'_id':md5.hexdigest()})
            if article == None:continue
            tokens = self._process_article(article)            
            if tokens == None:continue
            #xx.append(tokens)
            yield  tokens
        #return xx
    
    def _process_article(self, article):
        if article['title_pylxml'] != None and article['text_snacktory'] != None:
            text = '%//%'.join([article['title_pylxml'], article['text_snacktory']])
            if self.language == "en":                          
                tokens = en_Tokenize(text)
                tokens = self._en_filter(tokens)
            elif self.language == "en_zh":
                if article.has_key('translated'):
                    text=article['translated']
                else:
                    print text
                    text=self._en_zh_translate(text)
                    if text=="":return None
                    self.article_col.update({"_id":article["_id"]},{"$set":{"translated":text}})
                tokens = zh_Tokenize(text)
                tokens = self._zh_filter(tokens)
            else:
                tokens = zh_Tokenize(text)
                tokens = self._zh_filter(tokens)
            self.length += 1
            return tokens
        else:
            return None
        
    
    def _en_filter(self, tokens):
        res = []
        for token in tokens:
            token = lowcase_Filter(token)
            token = en_Stopword_Filter(token)
            if token == None:continue
            token = lemm_Filter(token)
            res.append(token)
        return res
    
    def _en_zh_translate(self,text):
        res=split_tran(sent_Tokenize(text),span=1000)
        print text
        print res
        return res
    
    
    def _zh_filter(self, tokens):
        res = []
        for token in tokens:
            token = zh_Stopword_Filter(token)
            if token == None:continue
            res.append(token)
        return res
    
    
    def get_texts(self):
        return self._get_topic()
    
    
