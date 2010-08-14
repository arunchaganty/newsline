#
# NewsLine Algorithm
#

import article
import count_articles_threaded
import get_articles_threaded
import make_queries
import newsitem
import select_articles
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

    # Expand based on subset matches of keywords
    ranked_keywords = make_queries.expand_queries_from_keywords(ranked_keywords, 4)
    ranked_keywords.sort(key=lambda x: x[1], reverse=True)
    ranked_keywords = ranked_keywords[:min(5,len(ranked_keywords))]

    articles = get_articles_threaded.get_articles([w for (w,r) in ranked_keywords])

    articles = [[newsitem.NewsItem(a) for a in group] for group in articles]

    # articles = select_best_articles.select_relevant_articles(articles, ranked_keywords)
    #articles = select_articles.select_all_articles(articles, ranked_keywords)
    articles = select_articles.select_temporal_starting_articles(articles, ranked_keywords)

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

