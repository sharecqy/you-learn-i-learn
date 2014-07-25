import os
import struct
import sys
import gzip
from log import log

class worditem(object):
    def __init__(self, wordstr, offset, size):
        self.wordstr = wordstr
        self.offset = offset
        self.size = size

    def __str__(self):
        return 'wordstr=%s, offset=%d, size=%d' % (self.wordstr, self.offset, self.size)


class dictmanager(object):
    def __init__(self):
        self.dicts=[]

    def query_word(self,word):
        res=[]
        for dic in self.dicts:
            item=dic.query_word(word)
            definition=dic.query_item(item)
            if definition:
                res.append([dic.get_name(),definition])
        return res

    def add_dict(self,adict):
        self.dicts.append(adict)

    def init_dict(self,path,addto_manager=True):
        dic = stardict(None, "".join([path,".ifo"]), \
                "".join([path,".idx"]), "".join([path,".dict.dz"]))
        dic.do_staging()
        dic.do_indexing()
        if addto_manager:
            self.add_dict(dic)
        else:
            return dic


    def get_dict(self, name):
        for dic in self.dicts:
            if dic.get_name() == name:
                return dic

        return None





class stardict(object):
    def __init__(self, uri, ifoloc, idxloc, dataloc):
        self.ifoloc = ifoloc
        self.idxloc = idxloc
        self.dataloc = dataloc
        if os.path.isfile(self.ifoloc):
            log.warn("ifo %s file is not exist" % self.ifoloc)
        elif os.path.isfile(self.idxloc):
            log.warn("idx %s file is not exist" % self.idxloc)
        elif os.path.isfile(self.dataloc):
            log.warn("data %s file is not exist" % self.dataloc)


        self.uri = uri
        self.wordlist = []
        self.wordcount = 0
        self.author = None
        self.name = None
        self.disabled = False
        self.priority = -1
        self.wordset=set()


    def is_default(self):
        if self.uri == 'default':
            return True
        return False

    def is_phonetic(self):
        if self.uri == 'phonetic':
            return True
        return False

    def is_addon(self):
        if self.uri not in ('default', 'phonetic'):
            return True
        return False

    def do_staging(self):
        # read dictionary ifo file
        log.info("parse stardict info file %s" % self.ifoloc)
        try:
            ifo = open(self.ifoloc, 'r')
        except IOError:
            log.warn("failed to open %s" % self.ifoloc)
            return False

        ifodata = {}
        for line in ifo.readlines():
            if line.find('=')<0:
                continue

            if line[-1] == '\n':
                line = line[:-1]
            k, v = line.split('=')
            ifodata[k] = v
        ifo.close()

        if ifodata.has_key('wordcount'):
            self.wordcount = int(ifodata['wordcount'])
        else:
            log.warn("wordcount is missing in %s" % self.ifoloc)
            return False

        if ifodata.has_key('bookname'):
            self.name = ifodata['bookname']
        else:
            log.warn("bookname is missing in %s" % self.ifoloc)
            return False

        return True

    def do_indexing(self):
        # read dictionary index file
        log.info("parse stardict index file %s" % self.idxloc)
        try:
            idx = open(self.idxloc, 'rb')
        except IOError:
            log.warn("failed to open %s" % self.idxloc)
            return False

        idxdata = idx.read()
        idx.close()

        start = 0
        for i in range(self.wordcount):
            pos = idxdata.find('\0', start, -1)
            fmt = "%ds" % (pos-start)
            wordstr = struct.unpack_from(fmt, idxdata, start)[0]
            start += struct.calcsize(fmt) + 1

            (off, size) = struct.unpack_from(">LL",idxdata, start)
            start += struct.calcsize(">LL")
            item = worditem(wordstr, off, size)
            self.wordset.add(wordstr)
            self.wordlist.append(item)

        log.info("identify dict %s, word count %d" % (self.name, self.wordcount))
        return True

    def get_wordset(self):
        return self.wordset

    def get_wordlist(self):
        return self.wordlist

    def get_wordcount(self):
        return self.wordcount

    def get_name(self):
        return self.name

    def get_uri(self):
        return self.uri
        
    def query_word(self, wordstr):
        start = 0
        end = self.wordcount-1

        while start <= end:
            mid = (start+end) >> 1
            res = cmp(wordstr, self.wordlist[mid].wordstr)
            if res == 0:
                return self.wordlist[mid]
            elif res > 0:
                start = mid + 1
            else:
                end = mid - 1

        return None


    def query_item(self, worditem):
        if not worditem:
            return None

        try:
            f =  gzip.open(self.dataloc, 'rb')
            f.seek(worditem.offset, 0)
        except IOError:
            log.warn("failed to open %s" % self.dataloc)
            return None

        text = f.read(worditem.size)
        f.close()

        return text


    def get_disabled(self):
        return self.disabled

    def set_disabled(self, option):
        self.disabled = option

    def get_priority(self):
        return self.priority

    def set_priority(self, p):
        self.priority = p


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)

    word = sys.argv[1]
    log.info("input word: %s" % word)

    mgr = starmanager()
    mgr.do_indexing()

    for dic in mgr.get_dicts():
        item = dic.query_word(word)
        if item:
            print dic.get_name()
            print dic.query_item(item)
            print ""
   