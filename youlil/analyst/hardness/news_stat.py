from nltk.tokenize import RegexpTokenizer,sent_tokenize
from pymongo import Connection, DESCENDING
from nltk.stem import WordNetLemmatizer
from  nltk.stem.lancaster import  LancasterStemmer
from nltk.stem import SnowballStemmer
from news_analyzer import MongoDBSequence
from news_analyzer import NewsHardnessAnalyzer
import enchant
enchant.set_param("enchant.myspell.dictionary.path","/usr/lib/python2.6/site-packages/pyenchant-1.6.5-py2.6.egg/enchant/share/enchant/myspell")
import operator
class Word_Stat:
    def __init__(self):
        self.words={}
        self.bigram={}
        self.tokenizer = RegexpTokenizer("[\w]+")
        self.lemmatizer = WordNetLemmatizer()
        self.lanstemmer = LancasterStemmer()
        self.stemmer = SnowballStemmer("english")
        self.dictionary = enchant.Dict("en_US")
        con = Connection()
        db = con['learner']
        self.news = db['news']

    def stat(self,news_count=10):
        news=self.read_news(news_count)
        for item in news:
            word_list=self.tokenize(item['text_snacktory'])
            for word in word_list:
                if self.digit_filter(word):continue
                self.add_word(self.lemm_filter(self.lowcase_filter(word)))
        self.words=self.dict_sort(self.words)
        file=open('word_stat.txt','w')
        for key,value in self.words:
            file.write('%s %d\n' %(key.encode('utf-8'),value))
        file.close()

    def bigram_stat(self,news_count=10):
        news=self.read_news(news_count)
        for item in news:
            word_list=self.tokenize(item['text_snacktory'])
            for i in range(len(word_list)-1):
                word1=self.lemm_filter(self.lowcase_filter(word_list[i]))
                word2=self.lemm_filter(self.lowcase_filter(word_list[i+1]))
                self.add_bigram((word1,word2))
        self.bigram=self.dict_sort(self.bigram)
        file=open('bigram_stat.txt','w')
        for key,value in self.bigram:
            file.write('%s %s %d\n' %(key[0].encode('utf-8'),key[1].encode('utf-8'),value))
        file.close()

    def read_news(self,news_count):
        return self.news.find({},{'text_snacktory':1}).limit(news_count)

    def tokenize(self,text):
        return self.tokenizer.tokenize(text)
    
    def digit_filter(self,word):
        for w in word:
            if w.isdigit():return True
        return False

    def lowcase_filter(self,word):
        return word.lower()

    def lemm_filter(self,word):
        #return self.lemmatizer.lemmatize(word)
        temp=self.lanstemmer.stem(word)
        if self.dictionary.check(temp):
            return temp
        else:
            temp=self.stemmer.stem(word)
            if self.dictionary.check(temp):
                return temp
            else:
                return self.lemmatizer.lemmatize(word)

    def add_bigram(self,big):
        self.bigram.setdefault(big,0)
        self.bigram[big]+=1

    def add_word(self,word):
        self.words.setdefault(word,0)
        self.words[word]+=1

    def dict_sort(self,adict):
        return sorted(adict.iteritems(), key=operator.itemgetter(1),reverse=True)
    

class Sent_Stat:
    def __init__(self):
        self._seq=MongoDBSequence()
        self._sent_tokenize=sent_tokenize

    def avg_sent_stat(self,count=1000):
        sum=0.0
        max=0
        for index,doc in enumerate(self._seq):
            if index==count:break
            sents=self._sent_tokenize(doc['text_snacktory'])
            print len(sents)
            if len(sents)>max:max=len(sents)
            sum+=len(sents)
        return sum/count,max


class News_Stat:
    def __init__(self):
        self._seq=MongoDBSequence()
        self._hardness_analyzer=NewsHardnessAnalyzer().news_hardness


    def score_distribute_stat(self,count=1000):
        dist={(-1000,0.5):0,(0.5,1):0,(1,1.5):0,(1.5,2):0,(2,2.5):0,(2.5,3):0,(3,3.5):0,(3.5,4):0,(4,4.5):0,(4.5,1000):0}
        invalid=0
        for doc in self._seq:
            if count:count-=1
            else:
                break
            score=self._hardness_analyzer(doc['title_pylxml'],doc['text_snacktory'])
            if score==False:
                print "an invalid news"
                invalid+=1
            for key,value in dist.items():
                if score>=key[0] and score<key[1]:
                    dist[key]+=1
                    break
        self._hardness_report(dist,invalid)

    def _hardness_report(self,dist,invalid):
        print "hardness report\n"
        for key,value in dist.items():
            print "news between %s and %s     is  %d" %(key[0],key[1],value)
        print "invalid news is %d" %invalid




        


#ws=Word_Stat()
#ws.stat(16000)
#ws.bigram_stat(1000)


