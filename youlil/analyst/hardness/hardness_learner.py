from nltk.tokenize import RegexpTokenizer,sent_tokenize,word_tokenize
from nltk.stem import WordNetLemmatizer
from  nltk.stem.lancaster import  LancasterStemmer
from nltk.stem import SnowballStemmer
from training_corpus import MongoDBSequence,RandomSentence
#from training_corpus import NewsHardnessAnalyzer
import enchant
enchant.set_param("enchant.myspell.dictionary.path","/usr/lib/python2.6/site-packages/pyenchant-1.6.5-py2.6.egg/enchant/share/enchant/myspell")
import operator
from numpy import array,zeros,linalg,sum,absolute,amax,column_stack
import random


class SentCorpus:
    """
        Prepare scored sentences
    """
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
        self.max_wordlen=0
        self.max_sentlen=0
        self.max_num_commar=0
        self.max_cet4_percent=0

    def init_cet4(self):
        with open('./data/cet4.txt','r') as f:
            words=[]
            for line in f.readlines():
                words.append(line.split()[0])
        return words


    def new_sents(self):
        return self._data
    
    def scored_sents(self):
        return self._sents_dict
    
  
    def store(self,filename='./data/sents_corpus'):
        f=open(filename,'w')
        for sent in self._data:
            sent=sent.replace('\n','')
            f.write("<<<%s\n" %sent.encode('utf-8'))
   
    def __len__(self):
        return len(self._sents_dict.items())

    def load(self,filename='./data/scored_sents.txt'):
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

class linear_learn:
    """
        Linear Regression
        >>>ll=linear_learn()
        >>>ll.learn()
    """
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

     

