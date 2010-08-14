#
# NewsLine Algorithm
#

import article
import count_articles
import extract
import get_articles
import make_queries
import util

import sys
import random

class NewsItem:
    def __init__(self, d):
        self.date = int(d['date'])
        self.url = d['url']
        self.body = d['body']
        self.title = d['title']

    def __cmp__(self, y):
        return self.date < y.date

    def __hash__(self):
        return self.title.__hash__()

    def __repr__(self):
        return "%10d %100s"%(self.date, self.title)

    def __str__(self):
        return "% 80s %10d"%(self.title, self.date)

def NewsLine(filename):
    a = article.read_article_from_file(filename)
    util.Log("Finished Reading Article.")
    k = extract.extract_keywords(a)
    util.Log("Finished Extracting Keywords.")
    ranked_keywords = extract.rank_keywords(a, k, 
        count_articles.count_articles)

    search_query = make_queries.MakeQueriesFromKeywords(ranked_keywords)
    articles = get_articles.get_articles(search_query)

    articles = [[NewsItem(a) for a in group] for group in articles]
    articles = choose_relevant_articles(articles, ranked_keywords)

    articles.sort(reverse=True)

    for a in articles:
        print a

    return

def choose_relevant_articles(articles, ranked_keywords):
    # Sort each of the set of articles by date
    for x in articles:
        x.sort(reverse=True)

    relevances = [b for (a, b) in ranked_keywords]
    probabilites = [x/sum(relevances) for x in relevances] + [0.2] * 10

    final_articles = set()

    for i in range(len(articles)):
        for y in articles[i]:
            final_articles.add(y)
            if random.uniform(0, 1) > probabilites[i]:
                break

    return list(final_articles)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage %s <article>"%(sys.argv[0])

    s = sys.argv[1]
    NewsLine(s)

