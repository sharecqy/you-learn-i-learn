'''
Created on 2012-10-23

@author: cqy
'''
import re
import chardet

def get_Encoding(page):
    text = re.sub('</?[^>]*>\s*', ' ', page)
    if not text.strip() or len(text) < 10:
        return 'ascii'
    try:
        enc = 'utf-8'
        diff = text.decode(enc, 'ignore').encode(enc)
        sizes = len(diff), len(text)
        if abs(len(text) - len(diff)) < max(sizes) * 0.01:
            #print '->', enc, '100%'
            return enc
    except UnicodeDecodeError:
        #import traceback;traceback.print_exc()
        pass
    res = chardet.detect(text)
    enc = res['encoding']
    #print '->', enc, "%.2f" % res['confidence']
    if enc == 'MacCyrillic':
        enc = 'cp1251'
    return enc

def build_Doc(page):
    enc = get_Encoding(page)
    
    page_enc = page.decode(enc, 'replace').encode('utf-8')
    page_enc=unicode(page, enc)
    return page_enc