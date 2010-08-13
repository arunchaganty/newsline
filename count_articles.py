import nytimes
import util
import yql

import threading

class CountArticleThread(threading.Thread):
    def __init__ (self, keyword, title_keyword=""):
        threading.Thread.__init__(self)
        self.keyword = keyword
        self.title_keyword = title_keyword
        self.count = 0

    def run(self):
       n = nytimes.NYTimes()
       self.count = nytimes.get_total_number_of_articles(
           n.get_counts(self.keyword, self.title_keyword))


def count_articles(search_queries):
    """ Takes a list of pairs [(keyword, title_keyword)] and returns a list of
        the number of articles. """

    counts = []
    threads = []
    for (k, t) in search_queries:
        thread = CountArticleThread(k, t)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        util.Log("Thread joined: %s"%(thread.keyword))
        counts.append(thread.count)
    return counts

