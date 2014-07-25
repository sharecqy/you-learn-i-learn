from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.tokenize import RegexpTokenizer,sent_tokenize
from nltk.stem import WordNetLemmatizer
from  nltk.stem.lancaster import  LancasterStemmer
from nltk.stem import SnowballStemmer
import enchant
enchant.set_param("enchant.myspell.dictionary.path","/usr/lib/python2.6/site-packages/pyenchant-1.6.5-py2.6.egg/enchant/share/enchant/myspell")
from numpy import array,zeros,linalg,sum,absolute,amax,column_stack
from analyst.settings import CET4_WORDS_PATH


class ArticleHardnessAnalyzer:
    """
        This class is in charge of evaluate the hardness of an English article
        which is the expection score of each sentences.
    """
    def __init__(self):
        self._sent_tokenize=sent_tokenize
        self._sent_hardness=SentHardnessAnalyzer().sent_hardness

    def article_hardness(self,title="",text="Hello World!",report=False):
        try:
            sents=self._sent_tokenize(text)
            if len(sents)==0:
                raise UnevaluatedException("Hardness of this article can't be evaluated")
            final_score=0.0
            minus=0
            for index,sent in enumerate(sents):
                sent_score=self._sent_hardness(sent,False)
                if sent_score==False:
                    minus+=1
                    continue
                final_score+=sent_score
            if (index+1-minus)==0:return False
            final_score/=(index+1-minus)
            if final_score<0:
                final_score=0
            elif final_score>5:
                final_score=5
            if report==True:
               self._hardness_report(title,text,final_score)
            return final_score
        except:
            raise UnevaluatedException("Hardness of this article can't be evaluated")

    def _hardness_report(self,title,text,score):
        print "title: %s\n" %title
        print "score: %f\n" %score
        print "text:\n"
        print "  %s" %text




class SentHardnessAnalyzer:
    """
        This class is in charge of evauluate the hardness of a English sentence.
    """
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

    def sent_hardness(self,sent,report=False):
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
        with open(CET4_WORDS_PATH,'r') as f:
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

class UnevaluatedException(Exception):
    pass
