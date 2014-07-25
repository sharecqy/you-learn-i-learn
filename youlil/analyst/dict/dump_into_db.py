#from pymongo import Connection, DESCENDING
from stardict import dictmanager
from settings import LANGDAO_DICT,LAZYWORM_DICT,OXFORD_DICT

#con = Connection()
#db = con["dictionary"]
dm=dictmanager()
dm.init_dict(LANGDAO_DICT)
dm.init_dict(LAZYWORM_DICT)
dm.init_dict(OXFORD_DICT)

def init_wordlist():
	wordset=set()
	for adict in dm.dicts:
		print len(adict.get_wordset())
		print adict.get_wordlist()[1855],adict.get_name()
		wordset=wordset | adict.get_wordset()
	print len(wordset)

init_wordlist()