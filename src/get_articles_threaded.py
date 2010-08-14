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
        self.results = n.get_results(self.keyword, self.title_keyword, rank="closest")
        return


def get_articles(search_queries):
    """ Takes a list of pairs [(keyword, title_keyword)] and returns a list of
        relevant articles. """

    results = []
    threads = []
    for k in search_queries:
        thread = GetArticleThread(k)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        util.Log("Thread joined: (%s, %s)"%(thread.keyword, thread.title_keyword))
        try:
            if thread.results.results() != None:
                try:
                    articles = thread.results.results()['results']
                except KeyError, e:
                    articles = None
                    
                if type(articles) == list:
                    results.append(articles)
                elif type(articles) == dict:
                    results.append([articles])

        except AttributeError, e:
            pass
    return results 

