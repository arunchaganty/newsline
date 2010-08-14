#
# NewsLine Algorithm
#

import article
import count_articles_threaded
import get_articles_threaded
import make_queries
import newsitem
import select_best_articles
import util

import sys

import calais
import nltkExtractor
#extractor = calais.Calais()
extractor = nltkExtractor.NLTKExtractor()

def NewsLine(filename):
    a = article.read_article_from_file(filename)
    util.Log("Finished Reading Article.")
    k = extractor.get_keywords(a)
    util.Log("Finished Extracting Keywords.")
    ranked_keywords = extractor.rank_keywords(k) 
    util.Log(ranked_keywords)

    search_query = make_queries.MakeQueriesFromKeywords(ranked_keywords)
    articles = get_articles_threaded.get_articles(search_query)

    articles = [[newsitem.NewsItem(a) for a in group] for group in articles]

    # articles = select_best_articles.select_relevant_articles(articles, ranked_keywords)
    articles = select_best_articles.select_all_articles(articles, ranked_keywords)

    articles.sort(reverse=True)

    for a in articles:
        print a

    return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage %s <article>"%(sys.argv[0])
        sys.exit(1)

    s = sys.argv[1]
    NewsLine(s)
