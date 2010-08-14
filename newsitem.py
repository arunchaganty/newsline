import util

class NewsItem:
    def __init__(self, d):
        self.date = int(d['date'])
        self.url = util.unicode_to_ascii(d['url'])
        self.title = util.unicode_to_ascii(d['title'])
        try:
          self.body = util.unicode_to_ascii(d['body'])
        except KeyError:
          self.body = self.title

    def __cmp__(self, y):
        return self.date < y.date

    def __hash__(self):
        return self.title.__hash__()

    def __repr__(self):
      s = "%10d \t \t %80s"%(self.date, self.title[:80])
      s += "\n"
      s += "%10s \t \t %100s"%("".rjust(10), self.url[:100])
      return s

    def __str__(self):
        return self.__repr__()

