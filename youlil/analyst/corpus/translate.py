'''
Created on 2012-10-25

@author: cqy
'''

#!/usr/bin/env python
# -*- coding: latin-1 -*-
import urllib2
import urllib
import multiprocessing
import chardet
from nltk.tokenize import RegexpTokenizer,sent_tokenize
text="""
Dutch Liberals, Labour vow austerity in coalition deal%//%THE HAGUE (Reuters) - Dutch Prime Minister Mark Rutte's Liberals agreed a coalition with the Labour Party on Monday and vowed to follow a path of austerity. 
"""

def translate(to_translate, to_language="zh_CN", language="auto"):
    '''Return the translation using google translate
    you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
    if you don't define anything it will detect it or use english by default
    Example:
    print(translate("salut tu vas bien?", "en"))
    hello you alright?'''
    try:
        agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
        before_trans = 'class="t0">'
        to_translate=to_translate.encode('utf-8')
        query={'hl':to_language,'sl':language,'q':to_translate}
        query_str=urllib.urlencode(query)
        link= "http://translate.google.com/m?%s" %query_str
        #link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_language, language, to_translate.replace(" ", "+"))
        request = urllib2.Request(link, headers=agents)
        page = urllib2.urlopen(request).read()
        result = page[page.find(before_trans)+len(before_trans):]
        result = result.split("<")[0]
    except:
        print "error"
        return ""
    return result


pools=multiprocessing.Pool(3)
def split_tran(sents,to_lang="zh_CN",from_lang="auto",span=1800):
    length=0
    para=[]
    content=[]
    temp=""  
    for sent in sents:
        if para==[]:
            para.append(temp)
            length+=len(temp)
        length+=len(sent)+1
        para.append(sent)
        if length>span and length<span+50:
            content.append(' '.join(para))
            length=0
            para=[]
            temp=""
        elif length>=span+50:
            break_point=para[-1].find(',')
            if break_point>50:break_point=50
            temp=para[-1][break_point:]
            para[-1]=para[-1][:break_point]
            content.append(' '.join(para))
            length=0
            para=[]
    if para!=[]:content.append(' '.join(para))
    """
    res=[]
    for t in content:
        res.append(translate(t))
    return ''.join(res)
    """
    results=[pools.apply_async(translate,[t]) for t in content]
    #results=pools.map(translate,content)
    res=[]
    for r in results:
        text=r.get()
        if text=='':continue
        res.append(unicode(text, chardet.detect(text).get('encoding','utf-8'),errors='ignore'))
    print res
    return ''.join(res)
    #res=pools.imap(translate,content)
    #for r in res:
    #    print r

if __name__ == '__main__':
    #tokens=text.split(' ')
    #print translate('hello google')
    sents=sent_tokenize(text)
    split_tran(sents,span=300)
