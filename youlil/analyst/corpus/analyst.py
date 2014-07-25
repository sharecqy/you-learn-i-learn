
'''
Created on 2012-10-25

@author: cqy
'''
from gensim import corpora, models, similarities
from mongocorpus import MongoCorpus
import operator
corpus = MongoCorpus(language='zh')
dictionary = corpus.dictionary
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

def tfidf():    
    rev_dict = {}
    for k, v in dictionary.token2id.items():
        rev_dict[v] = k


    for doc in corpus_tfidf:
        index=15
        print "==========="
        for key,value in sorted(doc, key=operator.itemgetter(1),reverse=True):
            print rev_dict[key], value
            index-=1
            if index==0:break


def lsi():
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) 
    return lsi.show_topics()                     
                          
def lda():
    lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=10, update_every=1, chunksize=10000, passes=1)
    for l in  lda.show_topics():
        print l

#lda()
tfidf()
