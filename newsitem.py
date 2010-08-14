import util
import re
import datetime

import pdb

class NewsItem:
    __date_re = re.compile("(\d{4})(\d{2})(\d{2})")

    def __init__(self, d):
        yyyymmdd = map(int, self.__date_re.match(d['date']).groups())
        self.date = datetime.date(*yyyymmdd)
        self.url = util.unicode_to_ascii(d['url'])
        self.title = util.unicode_to_ascii(d.get("title",""))
        self.body = util.unicode_to_ascii(d.get("body",""))
        
        if self.title == "" and self.body != "":
            self.title = self.body.splitlines()[0]
        elif self.body == "" and self.title != "":
            self.body = self.title
        elif self.body != "" and self.title != "":
            pass
        else:
            util.Log("%s epic-fail"%(self.url))

        return

    def __cmp__(self, y):
        return cmp(self.date, y.date)

    def __hash__(self):
        return self.title.__hash__()

    def __repr__(self):
      s = "%10s \t \t %80s"%(str(self.date), self.title[:80])
      s += "\n"
      s += "%10s \t \t %100s"%("".rjust(10), self.url[:100])
      return s

    def __str__(self):
        return self.__repr__()

