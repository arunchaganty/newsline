import util

class NewsItem:
    def __init__(self, d):
        self.date = int(d['date'])
        self.url = util.unicode_to_ascii(d['url'])
        self.body = util.unicode_to_ascii(d['body'])
        self.title = util.unicode_to_ascii(d['title'])

    def __cmp__(self, y):
        return self.date < y.date

    def __hash__(self):
        return self.title.__hash__()

    def __repr__(self):
        return "%10d %100s"%(self.date, self.title)

    def __str__(self):
        return self.__repr__()

