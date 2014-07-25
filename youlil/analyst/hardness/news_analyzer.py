from pymongo import Connection, DESCENDING
from random import choice
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem import WordNetLemmatizer
from  nltk.stem.lancaster import  LancasterStemmer
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer,sent_tokenize
import enchant
enchant.set_param("enchant.myspell.dictionary.path","/usr/lib/python2.6/site-packages/pyenchant-1.6.5-py2.6.egg/enchant/share/enchant/myspell")
class MongoDBSequence:
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




class SentCorpus:
    def __init__(self,sents_num=10):
        self._sents_dict={}
        self._sents_model={}
        self._data=RandomSentence(sents_num)
        self._cet4_words=self.init_cet4()
        self.tokenizer=  RegexpTokenizer('[\w]+')
        self.lemmatizer = WordNetLemmatizer()
        self.lanstemmer = LancasterStemmer()
        self.stemmer = SnowballStemmer("english")
        self.dictionary = enchant.Dict("en_US")
       
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
        self.max_wordlen=0
        self.max_sentlen=0
        self.max_num_commar=0
        self.max_cet4_percent=0

    def init_cet4(self):
        f=open('./data/cet4.txt','r')
        words=[]
        for line in f.readlines():
            words.append(line.split()[0])
        return words


    def new_sents(self):
        return self._data
    
    def scored_sents(self):
        return self._sents_dict
    '''
   
    '''
    def store(self,filename='./data/sents_corpus'):
        f=open(filename,'w')
        for sent in self._data:
            sent=sent.replace('\n','')
            f.write("<<<%s\n" %sent.encode('utf-8'))
   
    def __len__(self):
        return len(self._sents_dict.items())

    def load(self,filename='./data/scored_sents1.txt'):
        f=open(filename,'r')
        for sent in f.readlines():
            if sent.startswith('<<<'):
                continue
            temp=sent.split('<<<')
            try:
                self._sents_dict[temp[1]]=int(temp[0])
            except:
                print "error:%s is not an integer in %s" %(temp[0],sent)
        print len(self)
        return self._sents_dict

    def init_model(self):
        for key,value in self._sents_dict.items():
            self._sents_model[key]=(self._init_sent(key),value,0)
        return self._sents_model

    def _init_sent(self,sent):
        sent_model={}
        sent_list=word_tokenize(sent)
        word_list=self.tokenizer.tokenize(sent)
        sent_model['sent_length']=len(word_list)
        length=0.0
        num_commar=0.0
        num_cet4=0.0
        num_capital=-1.0
        for word in sent_list:
            length+=len(word) if word in word_list else 0
            if word ==',' or word==';':num_commar+=1
            if word and word[0].isupper():num_capital+=1
            if self.lemm_filter(word) in self._cet4_words:num_cet4+=1
        sent_model['avg_wordlen']=length/len(word_list)
        sent_model['num_commar']=num_commar
        sent_model['cet4_percent']=num_cet4/len(word_list)
        sent_model['num_capital']=num_capital
        return sent_model

    def lemm_filter(self,word):
        #return self.lemmatizer.lemmatize(word)$
        word=word.lower()
        temp=self.lanstemmer.stem(word)
        try:
            if self.dictionary.check(temp):
                return temp
            else:
                temp=self.stemmer.stem(word)
                if self.dictionary.check(temp):
                    return temp
                else:
                    return self.lemmatizer.lemmatize(word)
        except:
            return word

#sc=SentCorpus()
#sc.load()
#sc.init_cet4()
from numpy import array,zeros,linalg,sum,absolute,amax,column_stack
import random
class linear_learn:
    def __init__(self):
        self.matrix,self.target=self._init_data()

    def _init_data(self):
        sc=SentCorpus()
        sc.load()
        data=sc.init_model()
        data_length=len(data.items())
        param_length=5
        matrix=zeros((param_length,data_length),dtype=float)
        target=zeros(data_length,dtype=float)
        for index,value in enumerate(data.items()):
            matrix[0,index]=value[1][0]['sent_length']
            matrix[1,index]=value[1][0]['avg_wordlen']
            matrix[2,index]=value[1][0]['num_commar']
            matrix[3,index]=value[1][0]['cet4_percent']
            #matrix[4,index]=value[1][0]['num_capital']
            matrix[4,index]=1
            target[index]=value[1][1]
        matrix=self._normolize(matrix)
        return matrix,target

    def _normolize(self,matrix):
        self.max_array=amax(matrix,axis=1)
        return (matrix.T/self.max_array).T
        
    def _split_data(self,ratio=(300,50)):
        self.train_matrix=self.matrix[:,0:ratio[0]]
        self.test_matrix=self.matrix[:,ratio[0]:]
        self.train_target=self.target[0:ratio[0]]
        self.test_target=self.target[ratio[0]:]

    def _random_split_data(self,ratio=(5.0,1.0)):
        self.train_matrix=self.matrix[:,0]
        self.test_matrix=self.matrix[:,1]
        self.train_target=[self.target[0]]
        self.test_target=[self.target[1]]
        for index in range(self.matrix.shape[1]):
            if index==0 or index==1:continue
            if random.random()<(ratio[0]/sum(ratio)):
                self.train_matrix=column_stack((self.train_matrix,self.matrix[:,index]))
                self.train_target.append(self.target[index])
            else:
                self.test_matrix=column_stack((self.test_matrix,self.matrix[:,index]))
                self.test_target.append(self.target[index])
        #print self.train_matrix.shape,self.train_target.shape
    def train(self):
        #self._split_data()
        #print self.train_matrix.shape,self.train_target.shape
        self._random_split_data()
        #print self.train_matrix.shape,self.train_target.shape
        self.weight=linalg.lstsq(self.train_matrix.T,self.train_target)[0]
        return self.weight
    
    def learn(self,count=10):

        for i in range(count):
            if i==0:
                temp_weight=self.train()
                temp_test_target=self.test_target
                temp_test_matrix=self.test_matrix
                min=self.mean_error()
            else:
                self.train()
                res=self.mean_error()
                if res<min:
                    temp_weight=self.weight
                    temp_test_target=self.test_target
                    temp_test_matrix=self.test_matrix
                    min=res
        #print min
        self.weight=temp_weight
        self.test_matrix=temp_test_matrix
        self.test_target=temp_test_target
        self.mean_error()
        #return temp

    def mean_error(self):
        #print self.test_matrix.T.shape,self.weight.shape
        ans=sum(self.test_matrix.T*self.weight,axis=1)
        count=ans.shape[0]
        #print count
        #print self.test_target
        #print ans
        error=sum(absolute(self.test_target-ans),dtype=float)/count
        self.report(error, ans)
        return error

    def report(self,error,ans):
        print "max array:%s\n" %self.max_array
        print "target:%s\n" %self.test_target
        print "ans:%s\n" %ans
        print "weight:%s\n" %self.weight
        print "error%s\n" %error

    def final_report(self,min):
        print "min:%s" %min

        


class SentHardnessAnalyzer:
    def __init__(self):
        self._words_tokenizer=word_tokenize
        self._regex_tokenizer=RegexpTokenizer('[\w]+').tokenize
        self._cet4_words=self.init_cet4()
        self._lemmatizer = WordNetLemmatizer()
        self._lanstemmer = LancasterStemmer()
        self._stemmer = SnowballStemmer("english")
        self._dictionary = enchant.Dict("en_US")
        self.weight=array([-6.81083322,-2.27423893,4.67657679,0.38339826,5.65177923],dtype=float)
        self.max_array=array([101., 6.78571429,31.,1.,1.],dtype=float)

    def sent_hardness(self,sent,report=True):
        score=self._sent_hardness(sent)
        if score==False: return False
        if report==True:
            self.report(sent,score)
        return score

    def _sent_hardness(self,sent):
        matrix=zeros((5),dtype=float)
        target=0
        sent_list=self._words_tokenizer(sent)
        word_list=self._regex_tokenizer(sent)
        if len(word_list)==0 or len(sent_list)==0:
            return False
        length=0.0
        num_commar=0.0
        num_cet4=0.0
        num_capital=-1.0
        for word in sent_list:
            length+=len(word) if word in word_list else 0
            if word ==',' or word==';':num_commar+=1
            if word and word[0].isupper():num_capital+=1
            if self.lemm_filter(word) in self._cet4_words:num_cet4+=1
        matrix[0]=len(word_list)
        matrix[1]=length/len(word_list)
        matrix[2]=num_commar
        matrix[3]=num_cet4/len(word_list)
        matrix[4]=1

        #sent_model['num_capital']=num_capital
        return sum((matrix/self.max_array)*self.weight.T)
    
    def init_cet4(self):
        f=open('./data/cet4.txt','r')
        words=[]
        for line in f.readlines():
            words.append(line.split()[0])
        return words
    
    def lemm_filter(self,word):
        #return self.lemmatizer.lemmatize(word)$
        word=word.lower()
        temp=self._lanstemmer.stem(word)
        try:
            if self._dictionary.check(temp):
                return temp
            else:
                temp=self._stemmer.stem(word)
                if self._dictionary.check(temp):
                    return temp
                else:
                    return self._lemmatizer.lemmatize(word)
        except:
            return word
    
    def report(self,sent,score):
        print "sent:%s\n" %sent
        print "score:%f\n" %score

class NewsHardnessAnalyzer:
    def __init__(self):
        self._seq=MongoDBSequence()
        self._sent_tokenize=sent_tokenize
        self._sent_hardness=SentHardnessAnalyzer().sent_hardness

    def news_hardness(self,title="Hello",text="Hello World!",report=True):
        sents=self._sent_tokenize(text)
        if len(sents)==0:return False
        final_socre=0.0
        minus=0
        for index,sent in enumerate(sents):
            sent_score=self._sent_hardness(sent,False)
            if sent_score==False:
                minus+=1
                continue
            final_socre+=sent_score
        if (index+1-minus)==0:return False
        final_socre/=(index+1-minus)
        if report==True:
           self._hardness_report(title,text,final_socre)
        return final_socre

    def _hardness_report(self,title,text,score):
        print "title: %s\n" %title
        print "score: %f\n" %score
        print "text:\n"
        print "  %s" %text



        



