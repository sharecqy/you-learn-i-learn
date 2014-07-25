from stardict import dictmanager
from settings import LANGDAO_DICT,LAZYWORM_DICT,OXFORD_DICT
import sys
import log
"""
ifoloc="./dicts/default/oxford-gb-formated.ifo"
idxloc="./dicts/default/oxford-gb-formated.idx"
dataloc="./dicts/default/oxford-gb-formated.dict.dz"
"""


if __name__=="__main__":
    dm=dictmanager()
    dm.init_dict(LANGDAO_DICT)
    dm.init_dict(LAZYWORM_DICT)
    dm.init_dict(OXFORD_DICT)
    while True:
        word=raw_input("please input a word:")
        for d in dm.query_word(word):
            print d[0]
            print d[1]
            print "\n\n"
        


    