import nytimes
import util
import yql

import threading

class GetArticleThread(threading.Thread):
    def __init__ (self, keyword, title_keyword=""):
        threading.Thread.__init__(self)
        self.keyword = keyword
        self.title_keyword = title_keyword
        self.results = None

    def run(self):
        n = nytimes.NYTimes()
        self.results = n.get_results(self.keyword, self.title_keyword)
        return


def get_articles(search_queries):
    """ Takes a list of pairs [(keyword, title_keyword)] and returns a list of
        relevant articles. """

    results = []
    threads = []
    for (k, t) in search_queries:
        thread = GetArticleThread(k, t)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        util.Log("Thread joined: (%s, %s)"%(thread.keyword, thread.title_keyword))
        try:
            if thread.results.results() != None:
                results.append(thread.results.results()['results'])
        except AttributeError, e:
            pass
    return results 

